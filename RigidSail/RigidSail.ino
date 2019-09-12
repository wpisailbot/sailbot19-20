#include <WiFiEsp.h>
#include <WiFiEspUdp.h>
#include <Servo.h>
#include "SoftwareSerial.h"
#include "Comm_encoder.h"
#include "Constants.h"

// //Pins for devices
// #define potPin A19   //38
// #define servoPin 6
// #define led1Pin 7   //white
// #define led2Pin 8   //white
// #define wifiLED 5   //yellow
// #define powerLED 4  //red
// #define vInPin A2
// #define RX2pin 9    //ESP8266
// #define TX2pin 10   //ESP8266
// #define onBoardLED 13

// Servo variables
int control = 0;      //to enable direct control over tab angle
int lift = 0;         //0 to produce no lift 1 to produce lift
int drag = 0;
int windSide = 0;     //0 for wind from port 1 for wind from starboard
bool manual = false;

int heelIn;           //reading from hull heel sensor
int heelAngle = 0;    //mapped heel angle, 0 degrees is straight up 90 would be on its side
int maxHeelAngle = 30;//settable max heel angle

int angleIn;          //reading from wind direction sensor on the front of the sail
int windAngle;  //mapped value from wind sensor
int sentAttackAngle;  //value mapped to correct sending format

int controlAngle = 0; //manual angle set by boat

int tabAngle = 0;     //angle of tab relative to centered being 0

int count = 0;        //count to have leds blink

int state = MIN_LIFT;

int printing = 0;
int udpConnection = 0;
int connectionCount = 0;

int ledState = LOW;
unsigned long previousMillis = 0;
volatile unsigned long blinkCount = 0; // use volatile for shared variables

int servoAngle;

int vIn = 0;

IntervalTimer LEDtimer;
IntervalTimer servoTimer;
IntervalTimer commsTimer;

Servo servo;

bool ack_connected = false;

// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2

char ssid[] = "sailbot";        // Name of the hull network
char pass[] = "Passphrase123";  // Password to hull network
int status = WL_IDLE_STATUS;    // the Wifi radio's status

IPAddress hullIP(192, 168, 0, 21);  // Hull's IP address

unsigned long lastConnectionTime = 0;         // last time you connected to the server, in milliseconds
const unsigned long postingInterval = 10000L; // delay between updates, in milliseconds

// Initialize the Ethernet client object
char packetBuffer[255];          // buffer to hold incoming packet

vehicle_state_t rx_packet;
vehicle_state_t tx_packet = {5, 4, 3, 2, 1, 0};
vehicle_state_t * tx_packet_ptr = &tx_packet;

WiFiEspUDP Udp;



void setup()
{
  initComms();
  initServo();
}

void loop()
{
  // WIFI
  // if there are incoming bytes available
  // from the server, read them and print them
  // while (client.available()) {
  //   Serial.println("Client available");
  //   char c = client.read();
  //   Serial.write(c);
  // }

  // Read from Serial Terminal for state -- testing only
  if (Serial.available() > 0) {
    // read the incoming byte:
    state = Serial.read() - 48;

    Serial.print("State:");
    Serial.println(state);
  }

  // WIFI
  // if 10 seconds have passed since your last connection,
  // then connect again and send data
  // if (millis() - lastConnectionTime > postingInterval) {
  //   //httpRequest();
  // }

  vIn = analogRead(vInPin);

  if (windSide) {
    servoAngle = tabAngle + 60;
  }
  else {
    servoAngle = -tabAngle + 60;
  }
  sentAttackAngle = (360 + windAngle) % 360;

  stateSet((Trim_state)state);
}

void initComms()
{
  // initialize serial for debugging
  Serial.begin(115200);
  // initialize serial for ESP module
  // ESPSerial.begin(115200);
  // // initialize ESP module
  // WiFi.init(&ESPSerial);

  // // check for the presence of the shield
  // if (WiFi.status() == WL_NO_SHIELD) {
  //   Serial.println("WiFi shield not present");
  //   // don't continue
  //   while (true);
  // }

  // // attempt to connect to WiFi network
  // while ( status != WL_CONNECTED) {
  //   Serial.print("Attempting to connect to WPA SSID: ");
  //   Serial.println(ssid);
  //   // Connect to WPA/WPA2 network
  //   status = WiFi.begin(ssid, pass);
  // }

  // // you're connected now, so print out the data
  // Serial.println("Connected to wifi");
  // printWifiStatus();

  // Serial.println("\nStarting connection to server...");
  // // if you get a connection, report back via serial:
  // Udp.begin(localPort);
  
  // Serial.print("Listening on port ");
  // Serial.println(localPort);

  // udpConnection = 1;
}


void initServo() 
{
  //init
  pinMode(vInPin, INPUT);
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(wifiLED, OUTPUT);
  pinMode(powerLED, OUTPUT);
  pinMode(onBoardLED, OUTPUT);
  

  servo.attach(servoPin);

  LEDtimer.begin(blinkState, 916682);
  servoTimer.begin(servoControl, 50000);
  //commsTimer.begin(update_vehicle_state, 100000000);

  servo.write(SERVO_CTR); //in place so lift starts at 0 degrees or neutral state

  digitalWrite(powerLED, HIGH);// turn on power led
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

  digitalWrite(wifiLED, LOW);
}


void stateSet(Trim_state state) {
  switch (state)
  {
    case MIN_LIFT:
      control = 0;
      lift = 0;
      drag = 0;
      break;
    case STBD_TACK:
      control = 0;
      lift = 1;
      drag = 0;
      windSide = 1;
      break;
    case PORT_TACK:
      control = 0;
      lift = 1;
      drag = 0;
      windSide = 0;
      break;
    case MAX_DRAG_STBD:
      control = 0;
      lift = 0;
      drag = 1;
      windSide = 1;
      break;
    case MAX_DRAG_PORT:
      control = 0;
      lift = 0;
      drag = 1;
      windSide = 0;
      break;
    case MAN_CTRL:
      control = 1;
      lift = 0;
      drag = 0;
      break;
    
    default:
      break;
  }
}


void blinkState() {
  if (ledState == LOW) {
    ledState = HIGH;
    blinkCount = blinkCount + 1;  // increase when LED turns on
  } else {
    ledState = LOW;
  }
  if (!udpConnection) {
    digitalWrite(wifiLED, ledState);
  }
  if (lift) {
    if (windSide) {
      digitalWrite(led1Pin, HIGH);
      digitalWrite(led2Pin, LOW);
    }
    else {
      digitalWrite(led2Pin, LOW);
      digitalWrite(led1Pin, ledState);
    }
  }
  if (drag) {
    if (windSide) {
      digitalWrite(led2Pin, HIGH);
      digitalWrite(led1Pin, LOW);
    }
    else {
      digitalWrite(led1Pin, LOW);
      digitalWrite(led2Pin, ledState);
    }
  }
}


void servoControl() {
  angleIn = analogRead(potPin) - POT_HEADWIND; // reads angle of attack data
  angleIn = angleIn < 0 ? POT_HEADWIND + angleIn + (1023-POT_HEADWIND) : angleIn;
  
  windAngle = angleIn / 1023.0 * 360.0 - 180; // Convert to degrees, positive when wind from 0-180, negative when wind 180-359
  //---------------------------------------------------------------------------------------------------
  //set for manual control
  if (control) {
    digitalWrite(led1Pin, HIGH);
    digitalWrite(led2Pin, HIGH);
    servo.write(SERVO_CTR + controlAngle);
  }

  //------------------------------------------------------------------------------------------------------
  //when lift is desired
  if (lift) {

    if (!windSide) {
      windAngle = windAngle * -1;
    }

    //if the lift angle isnt enough and the heel angle isnt too much the angle of attack is increased
    if ((MAX_LIFT_ANGLE > windAngle+1)) {  //&& (abs(heelAngle) <= maxHeelAngle))) {
      if (tabAngle >= 55) { }
      else {
        tabAngle++;
      }
    }

    //if the lift angle is too much or the max heel angle is too much the sail lightens up
    else if ((MAX_LIFT_ANGLE < windAngle)) {  //&& (abs(heelAngle) <= maxHeelAngle)) || (abs(heelAngle) >= maxHeelAngle)) {
      if (tabAngle <= -55) {  }
      else {
        tabAngle--;
      }
    }

    //if the angle of attack is correct
    else if (MAX_LIFT_ANGLE == windAngle) { }

    //to adjust tab angle according to wind side
    if (windSide) {
      servo.write(SERVO_CTR + tabAngle);
    }
    else {
      servo.write(SERVO_CTR - tabAngle);
    }
  }
  //-----------------------------------------------------------------------------------------------------------
  //while drag if desired
  if (drag) {

    //set sail to most possible angle of attack with respect to direction of wind
    if (windSide) {
      servo.write(SERVO_CTR + 55);
    }
    else if (!windSide) {
      servo.write(SERVO_CTR - 55);
    }
  }
  //----------------------------------------------------------------------------------
  //minimum lift (weathervane)
  if (!lift && !drag && !control) {
    digitalWrite(led1Pin, LOW);
    digitalWrite(led2Pin, LOW);

    servo.write(SERVO_CTR);
  }
}



void update_vehicle_state()
{
  // if there's data available, read a rx_packet
  //Serial.println("Rx/Tx");
  int packetSize = Udp.parsePacket();
  if (packetSize) {
    Serial.print("Received rx_packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remoteIp = Udp.remoteIP();
    Serial.print(remoteIp);
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    // read the rx_packet into rx_packetBufffer
    int len = Udp.read(packetBuffer, 255);
    if (len > 0) {
      packetBuffer[len] = 0;
    }

    rx_packet = decode_msg(packetBuffer);
    Serial.println("Contents:");
    print_packet(rx_packet);

    // send a reply, to the IP address and port that sent us the rx_packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(encode_msg(tx_packet));
    Udp.endPacket();
  }

  if(!ack_connected){
    ack_connect();
  }
}

void ack_connect(){
  Udp.beginPacket(hullIP, Udp.remotePort());
  Udp.write("henlo?");
  Udp.endPacket();
  Serial.println("spam");

  int packetSize = Udp.parsePacket();
  ack_connected = packetSize > 0;
}
