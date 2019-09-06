/*
 WiFiEsp example: WebClient
 This sketch connects to google website using an ESP8266 module to
 perform a simple web search.
 For more details see: http://yaab-arduino.blogspot.com/p/wifiesp-example-client.html
*/

#include "WiFiEsp.h"

// Emulate ESPSerial on pins 6/7 if not present
//#ifndef HAVE_HWESPSerial
#include "SoftwareSerial.h"
SoftwareSerial ESPSerial(9, 10); // RX, TX
//#endif

char ssid[] = "sailbot";            // your network SSID (name)
char pass[] = "Passphrase123";        // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status

//char server[] = "192.168.0.25";
IPAddress server(192, 168, 0, 21);
int serverPort = 8888;

unsigned long lastConnectionTime = 0;         // last time you connected to the server, in milliseconds
const unsigned long postingInterval = 10000L; // delay between updates, in milliseconds

// Initialize the Ethernet client object
WiFiEspClient client;

void setup()
{
  // initialize serial for debugging
  Serial.begin(115200);
  // initialize serial for ESP module
  ESPSerial.begin(115200);
  setBaud("115200");
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
  Serial.println("You're connected to the network");
  
  printWifiStatus();

  Serial.println();
  Serial.println("Starting connection to server...");
  // if you get a connection, report back via serial
  if (client.connect(server, serverPort)) {
    delay(500);
    Serial.println("Connected to server");
    // Make a HTTP request
    client.println("GET /values HTTP/1.1");
    client.println("Host: 192.168.0.25:8888");
    client.println("Connection: keep-alive");
    client.println();
  }
}

void loop()
{
  // if there are incoming bytes available
  // from the server, read them and print them
  while (client.available()) {
    Serial.println("Client available");
    char c = client.read();
    Serial.write(c);
  }

  // if 10 seconds have passed since your last connection,
  // then connect again and send data
  if (millis() - lastConnectionTime > postingInterval) {
    httpRequest();
  }
}

// this method makes a HTTP connection to the server
void httpRequest()
{
  Serial.println();
    
  // close any connection before send a new request
  // this will free the socket on the WiFi shield
  client.stop();

  // if there's a successful connection
  if (client.connect(server, serverPort)) {
    delay(500);
    Serial.println("Connecting...");
    
    // send the HTTP PUT request
    client.println("GET /values HTTP/1.1");
    client.println("Host: 192.168.0.25:8888");
    client.println("Connection: keep-alive");
    client.println();

    // note the time that the connection was made
    lastConnectionTime = millis();
  }
  else {
    // if you couldn't make a connection
    Serial.println("Connection failed");
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

String setBaud(String baudrate){
  String tmpData = "";  //ensure it is empty
  ESPSerial.println("AT+UART_DEF=" + baudrate + ",8,1,0,0");
  delay(500);  //good value for wait = 500
  while (ESPSerial.available() >0 )  {
    char c = ESPSerial.read();
    tmpData += c;  // this is better for adding character
   }
   return tmpData;
}
