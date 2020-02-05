#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "comms.pb.h"

#include <WiFiEsp.h>
//#include <WiFiEspUdp.h>
#include "SoftwareSerial.h"
#include "Constants.h"
#include <Servo.h>

// Protobuf variables
volatile uint8_t rx_buffer[128];
volatile vessel_state rx_message;
// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2
char ssid[] = "sailbot";        // Name of the hull network
char pass[] = "Passphrase123";  // Password to hull network
int status = WL_IDLE_STATUS;    // the Wifi radio's status
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA};
WiFiEspClient client;
bool connection = false;
volatile int count = 0; //count to have leds blink
volatile int state = TRIM_STATE_MIN_LIFT;
volatile int ledState = LOW;
volatile unsigned long blinkCount = 0; // use volatile for shared variables
volatile int retryCount = 0;
IntervalTimer commsTimer;
IntervalTimer servoTimer;
volatile int missed_msgs = 0;



void setup()
{
    Serial.begin(115200);
    // initialize serial for ESP module
    ESPSerial.begin(115200);
    // initialize ESP module
    WiFi.init(&ESPSerial);
    establichConnection();
}



void loop() {
  simpleSendReceive();
}



void simpleSendReceive(){
  if(!connection){
    client.stop();
    establichConnection();
  }
  bool havePrinted = false;
  client.println("Hello BBB, I'm Teensy");
  while(client.available()){
    char c = client.read();
    Serial.print(c);
    havePrinted = true;
  } 
  if(havePrinted)
    Serial.println();
}



void establichConnection(){
  // check for the presence of the shield
  if (WiFi.status() == WL_NO_SHIELD) {
      Serial.println("WiFi shield not present");
      // don't continue
      while (true);
  }
  // attempt to connect to WiFi network
  while ( status != WL_CONNECTED) {
      Serial.print("Attempting to connect to WPA SSID: ");
      Serial.println(ssid);
      // Connect to WPA/WPA2 network
      status = WiFi.begin(ssid, pass);
  }
  // you're connected now, so print out the data
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  if(client.connect(hullIP, 50000)){
    Serial.println("Connected to server");
    client.print("Host: ");
    client.println(hullIP);
    client.println("Connection: keep-alive");
    client.println();
    connection = true;
  }
  Serial.print("Listening on port ");
  Serial.println(50000); 
  //commsTimer.begin(update_vehicle_state, 100000);
  missed_msgs = 0;
  retryCount = 0;
}



void clearConnection(){
  commsTimer.end();
  WiFi.disconnect();
  establichConnection();
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



//void update_vehicle_state()
//{
//  // if there's data available, read a rx_packet
//  int bytes = client.available();
//  //Serial.print("  Missed msgs:");
//  //Serial.println(missed_msgs);
//  Serial.print("Connected to ");
//  Serial.print(client.remoteIP());
//  Serial.print(", port ");
//  Serial.print(localPort);
//  Serial.print(", bytes: ");
//  Serial.println(bytes);
//  if(client.remoteIP() == IPAddress(0, 0, 0, 0)){
//    //recoverConnection();
//  }
//  missed_msgs++;
//  if (bytes > 0) {
//    if(client.remoteIP() == hullIP){
//      for(int i = 0; i < bytes; i++){
//        rx_buffer[i] = (uint8_t)client.read();
//      }
//      
//      rx_message = vessel_state_init_zero;
//      
//      pb_istream_t stream = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
//      bool status = pb_decode(&stream, vessel_state_fields, &rx_message);
//   
//      if (!status)
//      {
//          Serial.println("Failed to decode");
//          return;
//      }
//      if(rx_message.device_id != DEVICE_ID_ARDUINO){
//        Serial.println("Uknown Device");
//        client.flush();
//        missed_msgs++;
//        return;
//      }
//
//
//      missed_msgs = 0;
//      
//      Serial.print("  Device:");
//      Serial.print(rx_message.device_id);
//      Serial.print("  State:");
//      Serial.print(rx_message.state);
//      Serial.print("  curAngle:");
//      Serial.print(rx_message.curHeelAngle);
//      Serial.print("  maxAngle:");
//      Serial.print(rx_message.maxHeelAngle);
//      Serial.print("  ControlAngle:");
//      Serial.print(rx_message.controlAngle);
//      Serial.print("  WindAngle:");
//      Serial.print(rx_message.windAngle);
//      Serial.print("  vIn:");
//      Serial.print(rx_message.vIn);
//      Serial.print(" HallPort:");
//      Serial.print(rx_message.hallPortTrip);
//      Serial.print(" HallStbd:");
//      Serial.print(rx_message.hallPortTrip);
//      Serial.println();
//
//
//      state = rx_message.state;
//      //heelAngle = rx_message.curHeelAngle;
//      //maxHeelAngle = rx_message.maxHeelAngle;
//      //controlAngle = rx_message.controlAngle - 290;
//    } else {
//      //Serial.println("Unknown device!");
//      //client.flush();
//      missed_msgs++;
//    }
//  }
//  if(missed_msgs > 10){
//    client.stop();
//    Serial.println("Reconnecting client...");
//    connection = false;
//    commsTimer.end();
//  }
//}
