#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Comm_encoder.h>
#include <Constants.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};

IPAddress ip(192, 168, 0, 21);
IPAddress rigidIP(192, 168, 0, 25);
EthernetServer server(localPort);
EthernetUDP Udp;
char packetBuffer[255];          // buffer to hold incoming packet

vehicle_state_t rx_packet;
vehicle_state_t tx_packet = {0, 10, 20, 30, 40, 50};
vehicle_state_t * tx_packet_ptr = &tx_packet;

bool ack_connected = false;


void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  // Set up the server on the arduino
  Ethernet.begin(mac, ip);
  
   // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }
  
  //server.begin();

  // set up the udp connection to send messages to the teensy
  Udp.begin(localPort);
  
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
  Udp.beginPacket(rigidIP, Udp.remotePort());
  Udp.write("henlo?");
  Udp.endPacket();
  Serial.println("spam");

  int packetSize = Udp.parsePacket();
  ack_connected = packetSize > 0;
}
