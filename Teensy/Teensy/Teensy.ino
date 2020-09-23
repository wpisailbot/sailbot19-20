#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "TrimTabMessages.pb.h"

#include <WiFiEsp.h>
#include "SoftwareSerial.h"
#include "Constants.h"
#include <Servo.h>

// Protobuf variables
uint8_t rx_buffer[32];
unsigned char tx_buffer[32];

// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2
char ssid[] = "sailbot";                  // Name of the hull network
char pass[] = "Passphrase123";            // Password to hull network
int status = WL_IDLE_STATUS;              // the Wifi radio's status
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA};
WiFiEspClient client;
bool connection = false;
volatile int count = 0; //count to have leds blink

// Control variables
volatile int ledState = LOW;
volatile unsigned long blinkCount = 0; // use volatile for shared variables
volatile int vIn = 0;                  // Battery voltage
volatile int retryCount = 0;
IntervalTimer LEDtimer;
IntervalTimer servoTimer;
volatile int missed_msgs = 0;
Servo servo;
volatile float windAngle; // Mapped reading from wind direction sensor on the front of the sail
volatile int32_t control_angle;
bool readingNow = false;

int timeSinceLastComm = 0;
int timeout = 1000;

TrimState_TRIM_STATE state = TrimState_TRIM_STATE_MIN_LIFT;

void setup()
{
  // Show that we're on
  pinMode(powerLED, OUTPUT);
  digitalWrite(powerLED, HIGH);

  Serial.begin(115200);
  // initialize serial for ESP module
  ESPSerial.begin(115200);
  // initialize ESP module
  WiFi.init(&ESPSerial);
  //establishConnection();

  pinMode(vInPin, INPUT);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(wifiLED, OUTPUT);
  pinMode(onBoardLED, OUTPUT);

  servo.attach(servoPin);
  servo.write(SERVO_CTR);

  LEDtimer.begin(blinkState, 916682);

  servoTimer.begin(servoControl, 50000);
}

void loop()
{
  vIn = analogRead(vInPin);
  simpleSendReceive();
}

void simpleSendReceive()
{
  if (!connection)
  {
    client.stop();
    establishConnection();
  } else {
    if(!readingNow){
      writeProtobuf();
    }
    if(readingNow){
      readProtobuf();
    }
  }
}

void readProtobuf()
{
  // If there's data available, read a rx_packet
  int bytes = client.available();

  if (bytes){// Read the bytes into a buffer so that we can decode them
    for (int i = 0; i < bytes; i++)
    {
      rx_buffer[i] = (uint8_t)client.read();
    }
  
    // Prepare a struct to save the message to
    TrimState controlAngle = TrimState_init_zero;
  
    // Decode the message and save to a struct
    pb_istream_t stream_rx = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
    bool status_rx = pb_decode(&stream_rx, TrimState_fields, &controlAngle);
  
    // Couldn't decode the message, so want to reconnect
    if (!status_rx)
    {
      // Nothing read, so nothing to do
      Serial.println("Couldn't decode!");
      //return;
    }
  
    control_angle = (controlAngle.control_angle-980)*PWMScaler;
    state = controlAngle.state;
//    Serial.print("Control angle: ");
//    Serial.println(control_angle);
  
    missed_msgs = 0;
    readingNow = false;
    timeSinceLastComm = millis();
  }
}

void writeProtobuf()
{
  // Prep the message
  ApparentWind_Trim apparentWind = ApparentWind_Trim_init_zero;
  size_t message_length;

  // Create a stream that will write to the buffer
  pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));

  // Fill in the wind dir
  apparentWind.apparent_wind = windAngle;
//  apparentWind.apparent_wind = 3;

//  Serial.print("Wind Angle: ");
//  Serial.println(windAngle);
  
  // Encode the message
  bool status_tx = pb_encode(&stream_tx, ApparentWind_Trim_fields, &apparentWind);
  message_length = stream_tx.bytes_written;

  /* Then just check for any errors.. */
  if (!status_tx)
  {
    printf("Encoding failed: %s\n", PB_GET_ERROR(&stream_tx));
    return;
  }
  
  if(message_length > 0){
    int data =  client.write(tx_buffer, message_length);
//    Serial.print("Wrote: ");
//    Serial.println(data);
    if(data > 0){
      readingNow = true;
      timeSinceLastComm = millis();
    }
  }
}

void establishConnection()
{
  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD)
  {
    Serial.println("WiFi shield not present");
    // don't continue
    while (true)
      ;
  }
  // attempt to connect to WiFi network
  while (status != WL_CONNECTED)
  {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }
  // you're connected now, so print out the data
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  if (client.connect(hullIP, 50000))
  {
    Serial.println("Connected to server");
    connection = true;
  }
  Serial.print("Listening on port ");
  Serial.println(50000);
  missed_msgs = 0;
  retryCount = 0;
}

void clearConnection()
{
  WiFi.disconnect();
  establishConnection();
}

/**
 * @brief Sets the angle of the servo based on the angle of attack read from the encoder at the front
 * 
 */
void servoControl()
{
  // Read, format, and scale angle of attack reading from the encoder
  windAngle = analogRead(potPin) - POT_HEADWIND;                                            // reads angle of attack data and centers values on headwind
  windAngle = windAngle < 0 ? POT_HEADWIND + windAngle + (1023 - POT_HEADWIND) : windAngle; // wraps angle around
  windAngle = windAngle / 1023.0 * 360.0 - 180;                                             // Convert to degrees, positive when wind from 0-180, negative when wind 180-359

  // Set debug LEDs to on to indicate servo control is active
  digitalWrite(led1Pin, HIGH);
  digitalWrite(led2Pin, HIGH);

  // Write servo position to one read from the Arduino
  //  servo.write(SERVO_CTR + control_angle - 200 - 90);

  switch(state){
    case TrimState_TRIM_STATE_MAX_LIFT_PORT:
      //if the lift angle isnt enough and the heel angle isnt too much the angle of attack is increased
      if ((MAX_LIFT_ANGLE > windAngle+1)) {  //&& (abs(heelAngle) <= maxHeelAngle))) {
        if (control_angle >= 55) { }
        else {
          control_angle++;
        }
      }
    
      //if the lift angle is too much or the max heel angle is too much the sail lightens up
      else if ((MAX_LIFT_ANGLE < windAngle)) {  //&& (abs(heelAngle) <= maxHeelAngle)) || (abs(heelAngle) >= maxHeelAngle)) {
        if (control_angle <= -55) {  }
        else {
          control_angle--;
        }
      }
      servo.write(SERVO_CTR + control_angle - 200 - 90);
      break;
    case TrimState_TRIM_STATE_MAX_LIFT_STBD:
      windAngle*=-1;
      //if the lift angle isnt enough and the heel angle isnt too much the angle of attack is increased
      if ((MAX_LIFT_ANGLE > windAngle+1)) {  //&& (abs(heelAngle) <= maxHeelAngle))) {
        if (control_angle >= 55) { }
        else {
          control_angle++;
        }
      }
    
      //if the lift angle is too much or the max heel angle is too much the sail lightens up
      else if ((MAX_LIFT_ANGLE < windAngle)) {  //&& (abs(heelAngle) <= maxHeelAngle)) || (abs(heelAngle) >= maxHeelAngle)) {
        if (control_angle <= -55) {  }
        else {
          control_angle--;
        }
      }
      servo.write(SERVO_CTR + control_angle - 200 - 90);
      break;
    case TrimState_TRIM_STATE_MAX_DRAG_PORT:
      servo.write(SERVO_CTR - 55);
      break;
    case TrimState_TRIM_STATE_MAX_DRAG_STBD:
      servo.write(SERVO_CTR + 55);
      break;
    case TrimState_TRIM_STATE_MIN_LIFT:
      servo.write(SERVO_CTR);
      break;
    case TrimState_TRIM_STATE_MANUAL:
      servo.write(control_angle);
      break;
    default:
      servo.write(control_angle);
      break;
  }
}

void blinkState()
{
  // Toggle state
  ledState = ledState == LOW ? HIGH : LOW;

  digitalWrite(powerLED, ledState);

  // Blink WiFi led
  if (!connection)
  {
    digitalWrite(wifiLED, !ledState);
  }
  else
  {
    digitalWrite(wifiLED, HIGH);
  }

  switch(state){
    case TrimState_TRIM_STATE_MAX_LIFT_PORT:
      digitalWrite(led1Pin, HIGH);
      digitalWrite(led2Pin, LOW);
      break;
    case TrimState_TRIM_STATE_MAX_LIFT_STBD:
      digitalWrite(led1Pin, ledState);
      digitalWrite(led2Pin, LOW);
      break;
    case TrimState_TRIM_STATE_MAX_DRAG_PORT:
      digitalWrite(led1Pin, LOW);
      digitalWrite(led2Pin, HIGH);
      break;
    case TrimState_TRIM_STATE_MAX_DRAG_STBD:
      digitalWrite(led1Pin, LOW);
      digitalWrite(led2Pin, ledState);
      break;
    case TrimState_TRIM_STATE_MIN_LIFT:
      digitalWrite(led1Pin, LOW);
      digitalWrite(led2Pin, LOW);
      break;
    case TrimState_TRIM_STATE_MANUAL:
      digitalWrite(led1Pin, HIGH);
      digitalWrite(led2Pin, HIGH);
      break;
    default:
      digitalWrite(led1Pin, HIGH);
      digitalWrite(led2Pin, HIGH);
      break;
  }
}

void printWifiStatus()
{
  // print the SSID of the network you're attached to
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  // print your WiFi shield's IP address
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  // print the received signal strength
  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}
