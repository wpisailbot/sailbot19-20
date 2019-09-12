#ifndef Constants_h
#define Constants_h
#include <IPAddress.h>

/*  RIGID SAIL   */
/* Trim servo */
const int SERVO_UP_LIM = 30;
const int SERVO_CTR    = 115;
const int SERVO_LO_LIM = 180;
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

/*  COMMS   */
const char ack_buffer[] = "ACK"; // When comms worked out, change this to a protobuf with the ip of the device replying to
unsigned int localPort = 8888;
IPAddress hullIP(192, 168, 0, 21);  // Hull's IP address
IPAddress rigidIP(192, 168, 0, 25); // RigidSail's IP address

#endif