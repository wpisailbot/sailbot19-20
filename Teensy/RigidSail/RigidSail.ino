/**
 * @file RigidSail.ino
 * @author Irina Lavryonova (ilavryonova@wpi.edu)
 * @brief Code running the Teensy 3.6 controlling the trim tab
 * @version 0.1
 * @date 2019-11-11
 */
#include <WiFiEsp.h>
#include <WiFiEspClient.h>
#include <Servo.h>
#include "SoftwareSerial.h"
#include "Constants.h"

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "comms.pb.h"

// Wind servo variables
volatile int windAngle;       // Mapped reading from wind direction sensor on the front of the sail
Servo servo;

// Debugging variables
volatile int ledState = LOW;
volatile int vIn = 0;         // Battery voltage

// Interrupt variables
IntervalTimer LEDtimer;
IntervalTimer servoTimer;
//IntervalTimer commsTimer; // TODO: try reintroducing the timer so that we get the updates on a clock

// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2
char ssid[] = "sailbot";                  // Name of the hull network
char pass[] = "Passphrase123";            // Password to hull network
int status = WL_IDLE_STATUS;              // the Wifi radio's status
WiFiEspClient client;

// WiFi debug variables
volatile bool connection = false;
int missed_msgs = 0;
unsigned long lastConnectionTime = 0;         // last time you connected to the server, in milliseconds
const unsigned long postingInterval = 5L; // delay between updates, in milliseconds

// Protobuf variables
volatile uint8_t rx_buffer[128];
vessel_state rx_message;



/**
 * @brief Sets up the Teensy
 * Required method
 */
void setup()
{
  // turn on power led
  pinMode(powerLED, OUTPUT);
  digitalWrite(powerLED, HIGH);

  // Init comms and servo
  initComms();
  initServo();
}



/**
 * @brief Everything in this method gets called repeatedly
 * Required method
 */
void loop()
{
  // Read battery voltage
  vIn = analogRead(vInPin);

  // Time the cycles of the updates to the vessel state and the servo angle
  if(millis() - lastConnectionTime > postingInterval) {
    // Update vessel state
    update_vessel_state();
    // Update servo angle
    //servoControl(); // This is on a timer, no need to call here. Here only for debugging purposes.
    // Save time of last update
    lastConnectionTime = millis();
  }
}



/**
 * @brief Initializes communications, called in setup()
 * Required method
 */
void initComms()
{
  // Init serial - has to be 115200 in order to work with the ESP8266 WiFi module
  Serial.begin(115200);
  // Initialize serial for ESP module
  ESPSerial.begin(115200);
  // Initialize ESP module
  WiFi.init(&ESPSerial);

  // Check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    // Don't continue
    while (true)
      ;
  }

  // Attempt to connect to WiFi network
  while (status != WL_CONNECTED)
  {
    if(VERBOS_RIGID) {
      Serial.print("Attempting to connect to WPA SSID: ");
      Serial.println(ssid);
    }
    // Connect to WPA/WPA2 network
    status = WiFi.begin(ssid, pass);
  }

  // Connected to the WiFi, print the info if in verbose mode
  if(VERBOS_RIGID) {
    Serial.println("Connected to wifi");
    printWifiStatus();

    Serial.println("\nStarting connection to server...");
  }

  // Connect to the client (Arduino)
  clientConnect();

  if(VERBOS_RIGID) {
    Serial.print("Listening on port ");
    Serial.println(localPort);
  }
}



/**
 * @brief Initializes servo and debugging variables, starts interrupt timers, called in setup()
 * 
 */
void initServo()
{
  // Init pins
  pinMode(vInPin, INPUT);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(wifiLED, OUTPUT);
  pinMode(onBoardLED, OUTPUT);

  // Attach the trim tab servo
  servo.attach(servoPin);

  // Put servo and led updates on a timer
  LEDtimer.begin(blinkState, 916682);
  servoTimer.begin(servoControl, 50000);
  //commsTimer.begin(update_vessel_state, 100000); //TODO: try this again, perhaps with 30hz or so

  // Initialize servo position to neutral (no lift) so that the boat doesn't run away
  servo.write(SERVO_CTR);
}



/**
 * @brief Connects to the client, called in setup() and whenever connection is lost
 * 
 */
void clientConnect(){
  // Ensure that the queue is empty and the client has nothing for us
  client.flush();
  client.stop();

  // Connect to the Arduino
  if (client.connect(hullIP, localPort)) {
    // Print info about the client if verbose
    if(VERBOS_RIGID) {
      Serial.println("Connected to server");
      client.print("Host: ");
      client.println(hullIP);
      client.println("Connection: close");
      client.println();
    }

    // Update monitoring variable and the LED
    connection = true;
    digitalWrite(wifiLED, HIGH);
  }
}



/**
 * @brief Print the status of the WiFi, used for debugging only
 * 
 */
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



/**
 * @brief Toggles the state of some LEDs on a timer
 * 
 */
void blinkState()
{
  // Toggle state
  ledState = ledState == LOW ? HIGH : LOW;

  // Blink WiFi led
  if (!connection) {
    digitalWrite(wifiLED, ledState);
  } 
}



/**
 * @brief Sets the angle of the servo based on the angle of attack read from the encoder at the front
 * 
 */
void servoControl()
{
  // Read, format, and scale angle of attached reading from the encoder
  windAngle = analogRead(potPin) - POT_HEADWIND; // reads angle of attack data
  windAngle = windAngle < 0 ? POT_HEADWIND + windAngle + (1023 - POT_HEADWIND) : windAngle;
  windAngle = windAngle / 1023.0 * 360.0 - 180; // Convert to degrees, positive when wind from 0-180, negative when wind 180-359

  // Set debug LEDs to on to indicate servo control is active
  digitalWrite(led1Pin, HIGH);
  digitalWrite(led2Pin, HIGH);

  // Write servo position to one read from the Arduino
  servo.write(SERVO_CTR + rx_message.controlAngle-200  - 90);
}



/**
 * @brief Reads vessel state from the Arduino server
 * 
 * @TODO: make a response
 */
void update_vessel_state()
{
    // If there's data available, read a rx_packet
    int bytes = client.available();

    if(VERBOSE_RIGID){Serial.println(bytes);}

    // Message size determined by the protobuf struct, so possible to check if the bytes available constitute a full message
    if(bytes > 50) {
      // The queue is flooded, so we want to flush it
      client.flush();
      missed_msgs++;

      // Reconnect if the queue keeps getting flooded
      if(missed_msgs > 100) {
        clientConnect();
        missed_msgs = 0;
      }

      // Nothing read, so nothing to do
      return;

    } else if(bytes < 5) {
      // Message received is too small to be a protobuf message
      missed_msgs++;
      // Reconnect if keep getting really small messages
      if(missed_msgs > 100) {
        clientConnect();
        missed_msgs = 0;
      }
      return;
    }
    
    // Read the bytes into a buffer so that we can decode them
    for (int i = 0; i < bytes; i++) {
      rx_buffer[i] = (uint8_t)client.read();
    }

    // Prepare a struct to save the message to
    rx_message = vessel_state_init_zero;

    // Decode the message and saved to a struct
    pb_istream_t stream_rx = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
    bool status_rx = pb_decode(&stream_rx, vessel_state_fields, &rx_message);

    // Couldn't decode the message, so want to reconnect
    if (!status_rx) {
      if(VERBOS_RIGID) {Serial.println("Failed to decode");}
      clientConnect();
      //missed_msgs++;

      // Nothing read, so nothing to do
      return;
    }
    missed_msgs = 0;

    //blinkState(); //  This is on a timer, no need to call here. Here only for debugging purposes.

    if(VERBOSE_RIGID) {printPacket(rx_message);}
}