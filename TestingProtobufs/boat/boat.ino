#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "test.pb.h"
#include "Constants.h"

#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>
#include <EthernetUdp.h>

uint8_t tx_buffer[128];

vehicle_state tx_message;

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};

EthernetServer server(localPort);
//EthernetUDP Udp;

bool handshake = false;

void setup()
{
    Serial.begin(9600);
    while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    }
    // Set up the server on the arduino
    Ethernet.begin(mac, hullIP);

    // Check for Ethernet hardware present
    if (Ethernet.hardwareStatus() == EthernetNoHardware) {
        Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
        while (true) {
            delay(1); // do nothing, no point running without Ethernet hardware
        }
    }

    server.begin();

    Serial.print("server is at ");
    Serial.println(Ethernet.localIP());
    Serial.print("UDP communication is located at port ");
    Serial.println(localPort);
}
void loop() {
    update_vehicle_state();
}


void update_vehicle_state()
{
    EthernetClient client = server.available();
    if(!client.connected()){
      Serial.println("Client disconnected!");
      // Set up the server on the arduino
      Ethernet.begin(mac, hullIP);
  
      // Check for Ethernet hardware present
      if (Ethernet.hardwareStatus() == EthernetNoHardware) {
          Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
          while (true) {
              delay(1); // do nothing, no point running without Ethernet hardware
          }
      }
  
      server.begin();
  
      Serial.print("server is at ");
      Serial.println(Ethernet.localIP());
      Serial.print("UDP communication is located at port ");
      Serial.println(localPort);
    }
    //if(client == true){
        tx_message = vehicle_state_init_zero;
        tx_message.state = TRIM_STATE_MAN_CTRL;
        tx_message.curHeelAngle = 80;
        tx_message.maxHeelAngle = 90;
        tx_message.controlAngle = 20;
        tx_message.windAngle = 10;
        tx_message.vIn = 33;

        Serial.print("  State:");
        Serial.print(tx_message.state);
        Serial.print("  curAngle:");
        Serial.print(tx_message.curHeelAngle);
        Serial.print("  maxAngle:");
        Serial.print(tx_message.maxHeelAngle);
        Serial.print("  ControlAngle:");
        Serial.print(tx_message.controlAngle);
        Serial.print("  WindAngle:");
        Serial.print(tx_message.windAngle);
        Serial.print("  vIn:");
        Serial.print(tx_message.vIn);
        Serial.println();

        pb_ostream_t stream = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
        bool status = pb_encode(&stream, vehicle_state_fields, &tx_message);
    
        if (!status)
        {
            Serial.println("Failed to encode");
            return;
        }

        // check message content
//        Serial.println(stream.bytes_written);
//        for (uint8_t i = 0; i < stream.bytes_written; i++) {
//            Serial.print(tx_buffer[i],HEX);
//            Serial.print(F("-"));
//        }
//        Serial.println();
        server.write(tx_buffer, stream.bytes_written);
    //}
}

void send_hello()
{
    if(!handshake){
      server.write("HANDSHAKE");
    }
    EthernetClient client = server.available();
    int bytes = client.available();
    if(bytes > 0){
        Serial.print("Received rx_packet of size ");
        Serial.println(bytes);
        Serial.print("From ");
        Serial.print(client.remoteIP());
        Serial.print(", port ");
        Serial.println(client.remotePort());
        char msg[bytes];
        for(int i = 0; i < bytes; i++){
          char c = client.read();
          
          msg[i] = c;
        }
        if(strncmp(msg, ack_buffer, bytes) == 0){
          Serial.println("Handshake: successful");
          handshake = true;
          server.write(ack_buffer);
          delay(100);
        }
        Serial.println();
        
    }
}
