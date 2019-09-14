#ifndef Constants_h
#define Constants_h
#include <IPAddress.h>

/*  RIGID SAIL   */
/* Trim servo */
const int SERVO_LO_LIM = 30;
const int SERVO_CTR    = 115;
const int SERVO_HI_LIM = 180;
/* Wind vein*/
const int POT_HEADWIND = 463;
const bool POT_CLOCKWISE  = true;
/* State angles */
const int MAX_LIFT_ANGLE = 30;
/* Pins */
//Pins for devices
const int potPin    = 38;   //A19
const int servoPin  = 6;
const int led1Pin   = 7;    //white
const int led2Pin   = 8;    //white
const int wifiLED   = 5;    //yellow
const int powerLED  = 4;    //red
const int vInPin    = 16;   //A2
const int RX2pin    = 9;    //ESP8266
const int TX2pin    = 10;   //ESP8266
const int onBoardLED = 13;

/*  BOAT    */
const int hallPortPin = 4;
const int hallStbdPin = 5;

const int PWM1Pin = digitalPinToInterrupt(2); // state 1
const int PWM2Pin = digitalPinToInterrupt(3); // ballast
const int PWM3Pin = digitalPinToInterrupt(20); // rudder
const int PWM4Pin = digitalPinToInterrupt(21); 
const int PWM5Pin = digitalPinToInterrupt(19); // manual control
const int PWM6Pin = digitalPinToInterrupt(18); // state 2

const int HERO_pin1 = 9; // TODO:NEED TO UPDATE
const int HERO_pin2 = 10; // TODO:NEED TO UPDATE
//PWM range 980 - 2004

/*  COMMS   */
const char ack_buffer[] = "ACK"; // When comms worked out, change this to a protobuf with the ip of the device replying to
unsigned int localPort = 8888;
IPAddress hullIP(192, 168, 0, 21);  // Hull's IP address
IPAddress rigidIP(192, 168, 0, 25); // RigidSail's IP address
byte rigidMac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA};
byte boatMac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

#endif