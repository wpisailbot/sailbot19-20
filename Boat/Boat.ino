#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>
#include <EthernetUdp.h>

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};

Servo servo;

const int servo_pin = 9;

IPAddress ip(192, 168, 0, 21);

EthernetServer server(8888);

EthernetUDP Udp;

unsigned int localPort = 8888;

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
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
  }
  
  server.begin();

  // set up the udp connection to send messages to the teensy
  Udp.begin(localPort);
  
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
  Serial.print("UDP communication is located at port ");
  Serial.println(localPort);
}

void loop() {
  // listen for incoming clients
  int udpStatus = Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  if(udpStatus){
    //Serial.println("there was a problem resolving the hostname or port");
    Serial.print("RemoteIP: ");
    Serial.print(Udp.remoteIP());
    Serial.print(" RemotePort: ");
    Serial.println(Udp.remotePort());
  }
 
  EthernetClient client = server.available();
  
  if (client) {
    // send a UDP message to the teensy
    Udp.write("hello");
  
    // create the http page  
    Serial.println("new client");
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == '\n' && currentLineIsBlank) {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");
          client.println("Refresh: 5");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.print("<h1>Output Values</h1>");
          for (int digitalChannel = 2 ; digitalChannel < 10; digitalChannel++) {
            int sensorReading = digitalRead(digitalChannel);
            client.print("Output value ");
            client.print(digitalChannel);
            client.print(" is ");
            client.print(sensorReading);
            client.println("<br />");
          }
          client.println("</html>");
          break;
        }
        if (c == '\n') {
          currentLineIsBlank = true;
        } else if (c != '\r') {
          currentLineIsBlank = false;
        }
      }
    }
    delay(1);
    Udp.endPacket();
    Serial.println("sent same UDP packet");
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
  }
}
