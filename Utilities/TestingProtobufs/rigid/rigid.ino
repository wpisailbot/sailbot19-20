
#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "comms.pb.h"

#include <WiFiEsp.h>
//#include <WiFiEspUdp.h>
#include "SoftwareSerial.h"
#include "Constants.h"

// Protobuf variables
uint8_t rx_buffer[128];
vessel_state rx_message;


// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2
char ssid[] = "sailbot";        // Name of the hull network
char pass[] = "Passphrase123";  // Password to hull network
int status = WL_IDLE_STATUS;    // the Wifi radio's status
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA};
//WiFiEspUDP Udp;
WiFiEspClient client;

bool connection = false;

IntervalTimer commsTimer;

int missed_msgs = 0;

void setup()
{
    Serial.begin(115200);
    // initialize serial for ESP module
    ESPSerial.begin(115200);
    // initialize ESP module
    WiFi.init(&ESPSerial);

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
    // if you get a connection, report back via serial:
    //Udp.begin(localPort);

    if(client.connect(hullIP, localPort)){
      Serial.println("Connected to server");
      client.print("Host: ");
      client.println(hullIP);
      client.println("Connection: keep-alive");
      client.println();
      connection = true;
    }
    
    Serial.print("Listening on port ");
    Serial.println(localPort);  

    commsTimer.begin(update_vehicle_state, 100000);

    
}
void loop() {
  if(!connection){
    client.stop();
    Serial.println("Not connected");
    if(client.connect(hullIP, localPort)){
      connection = true;
      Serial.println("Connected to server");
      client.print("Host: ");
      client.println(hullIP);
      client.println("Connection: keep-alive");
      client.println();
      commsTimer.begin(update_vehicle_state, 100000);
    }
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


void update_vehicle_state()
{
  // if there's data available, read a rx_packet
  int bytes = client.available();
  Serial.print("  Missed msgs:");
  Serial.println(missed_msgs);
  missed_msgs++;
  if (bytes > 0) {
//    Serial.print("Received rx_packet of size ");
//    Serial.println(bytes);
//    Serial.print("From ");
//    Serial.print(client.remoteIP());
//    Serial.print(", port ");
//    Serial.println(localPort);
    if(client.remoteIP() == hullIP){
      missed_msgs = 0;
      for(int i = 0; i < bytes; i++){
        rx_buffer[i] = (uint8_t)client.read();
      }
      
      rx_message = vessel_state_init_zero;
  //    rx_buffer[0] = 0x08;
  //    rx_buffer[1] = 0x05;
  //    rx_buffer[2] = 0x10;
  //    rx_buffer[3] = 0x50;
  //    rx_buffer[4] = 0x18;
  //    rx_buffer[5] = 0x5A;
  //    rx_buffer[6] = 0x20;
  //    rx_buffer[7] = 0x14;
  //    rx_buffer[8] = 0x28;
  //    rx_buffer[9] = 0x0A;
  //    rx_buffer[10] = 0x30;
  //    rx_buffer[11] = 0x21;
      
      pb_istream_t stream = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
      bool status = pb_decode(&stream, vessel_state_fields, &rx_message);
   
      if (!status)
      {
          Serial.println("Failed to decode");
          return;
      }
      
      Serial.print("  State:");
      Serial.print(rx_message.state);
      Serial.print("  curAngle:");
      Serial.print(rx_message.curHeelAngle);
      Serial.print("  maxAngle:");
      Serial.print(rx_message.maxHeelAngle);
      Serial.print("  ControlAngle:");
      Serial.print(rx_message.controlAngle);
      Serial.print("  WindAngle:");
      Serial.print(rx_message.windAngle);
      Serial.print("  vIn:");
      Serial.print(rx_message.vIn);
      Serial.println();
    } else {
      //Serial.println("Unknown device!");
      client.flush();
      missed_msgs++;
    }
  }
  if(missed_msgs > 10){
    client.stop();
    Serial.println("Reconnecting client...");
    connection = false;
    commsTimer.end();
  }
}


void receive_hello(){
  //int packetSize = Udp.parsePacket();
  if(!client.connected()){
    client.stop();
    Serial.println("Not connected");
    if(client.connect(hullIP, localPort)){
      Serial.println("Connected to server");
      client.print("Host: ");
      client.println(hullIP);
      client.println("Connection: keep-alive");
      client.println();
    }
  }
  
  int bytes = client.available();
  if (bytes > 0) {
    
    Serial.print("Received rx_packet of size ");
    Serial.println(bytes);
    Serial.print("From ");
    Serial.print(client.remoteIP());
    Serial.print(", port ");
    Serial.println(localPort);

    //Serial.print("  Message:");
    char msg[bytes];
    for(int i = 0; i < bytes; i++){
      char c = client.read();
      
      msg[i] = c;
    }
    Serial.println();
    if(strncmp(msg, "HANDSHAKE", bytes) == 0){
      client.write(ack_buffer);
    }
    if(strncmp(msg, ack_buffer, bytes) == 0){
      Serial.println("Handshake: successful");
      connection = true;
      commsTimer.begin(update_vehicle_state, 100000);
    }
  }
}
