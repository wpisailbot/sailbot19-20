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


Servo servo;

// Wifi variables
SoftwareSerial ESPSerial(RX2pin, TX2pin); // RX2, TX2
char ssid[] = "sailbot";        // Name of the hull network
char pass[] = "Passphrase123";  // Password to hull network
int status = WL_IDLE_STATUS;    // the Wifi radio's status
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEA};
//WiFiEspUDP Udp;
WiFiEspClient client;

bool connection = false;




// Servo variables
volatile int control = 0; //to enable direct control over tab angle
volatile int lift = 0;    //0 to produce no lift 1 to produce lift
volatile int drag = 0;
volatile int windSide = 0; //0 for wind from port 1 for wind from starboard

volatile int heelAngle = 0;     //mapped heel angle, 0 degrees is straight up 90 would be on its side
volatile int maxHeelAngle = 30; //settable max heel angle

volatile int angleIn;         //reading from wind direction sensor on the front of the sail
volatile int windAngle;       //mapped value from wind sensor
volatile int sentAttackAngle; //value mapped to correct sending format

volatile int controlAngle = 0; //manual angle set by boat

volatile int tabAngle = 0; //angle of tab relative to centered being 0

volatile int count = 0; //count to have leds blink

volatile int state = TRIM_STATE_MIN_LIFT;

volatile int ledState = LOW;
volatile unsigned long blinkCount = 0; // use volatile for shared variables

volatile int servoAngle;

volatile int vIn = 0;

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

    servo.attach(servoPin);
    
    //servoTimer.begin(servoControl, 50000);
    commsTimer.begin(update_vehicle_state, 100000);

    servo.write(SERVO_CTR);    
}
void loop() {
  if(!connection){
    client.stop();
    Serial.println("Not connected");
    retryCount++;
    //if(retryCount < 25){
      if(client.connect(hullIP, localPort)){
        retryCount = 0;
        connection = true;
        Serial.println("Connected to server");
        client.print("Host: ");
        client.println(hullIP);
        client.println("Connection: keep-alive");
        client.println();
        commsTimer.begin(update_vehicle_state, 100000);
      }
    //}
//      if(retryCount > 5){
//        clearConnection();
//      }
  }

  vIn = analogRead(vInPin);

  if (windSide)
  {
    servoAngle = tabAngle + 60;
  }
  else
  {
    servoAngle = -tabAngle + 60;
  }
  sentAttackAngle = (360 + windAngle) % 360;

  stateSet((_TRIM_STATE)state);

  servoControl();
}

void clearConnection(){
  commsTimer.end();
  WiFi.disconnect();
  //WiFi.init(&ESPSerial);

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
    missed_msgs = 0;
    retryCount = 0;
}

void stateSet(_TRIM_STATE state)
{
  switch (state)
  {
  case TRIM_STATE_MIN_LIFT:
    control = 0;
    lift = 0;
    drag = 0;
    break;
  case TRIM_STATE_STBD_TACK:
    control = 0;
    lift = 1;
    drag = 0;
    windSide = 1;
    break;
  case TRIM_STATE_PORT_TACK:
    control = 0;
    lift = 1;
    drag = 0;
    windSide = 0;
    break;
  case TRIM_STATE_MAX_DRAG_STBD:
    control = 0;
    lift = 0;
    drag = 1;
    windSide = 1;
    break;
  case TRIM_STATE_MAX_DRAG_PORT:
    control = 0;
    lift = 0;
    drag = 1;
    windSide = 0;
    break;
  case TRIM_STATE_MAN_CTRL:
    control = 1;
    lift = 0;
    drag = 0;
    break;

  default:
    break;
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
  //Serial.print("  Missed msgs:");
  //Serial.println(missed_msgs);
  Serial.print("Connected to ");
  Serial.print(client.remoteIP());
  Serial.print(", port ");
  Serial.print(localPort);
  Serial.print(", bytes: ");
  Serial.println(bytes);
  if(client.remoteIP() == IPAddress(0, 0, 0, 0)){
    //recoverConnection();
  }
  missed_msgs++;
  if (bytes > 0) {
    if(client.remoteIP() == hullIP){
      for(int i = 0; i < bytes; i++){
        rx_buffer[i] = (uint8_t)client.read();
      }
      
      rx_message = vessel_state_init_zero;
      
      pb_istream_t stream = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
      bool status = pb_decode(&stream, vessel_state_fields, &rx_message);
   
      if (!status)
      {
          Serial.println("Failed to decode");
          return;
      }
      if(rx_message.device_id != DEVICE_ID_ARDUINO){
        Serial.println("Uknown Device");
        client.flush();
        missed_msgs++;
        return;
      }


      missed_msgs = 0;
      
      Serial.print("  Device:");
      Serial.print(rx_message.device_id);
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
      Serial.print(" HallPort:");
      Serial.print(rx_message.hallPortTrip);
      Serial.print(" HallStbd:");
      Serial.print(rx_message.hallPortTrip);
      Serial.println();


      state = rx_message.state;
      heelAngle = rx_message.curHeelAngle;
      maxHeelAngle = rx_message.maxHeelAngle;
      controlAngle = rx_message.controlAngle - 290;
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

void servoControl()
{
  angleIn = analogRead(potPin) - POT_HEADWIND; // reads angle of attack data
  angleIn = angleIn < 0 ? POT_HEADWIND + angleIn + (1023 - POT_HEADWIND) : angleIn;

  windAngle = angleIn / 1023.0 * 360.0 - 180; // Convert to degrees, positive when wind from 0-180, negative when wind 180-359
  //---------------------------------------------------------------------------------------------------
  //set for manual control
  if (control)
  {
    digitalWrite(led1Pin, HIGH);
    digitalWrite(led2Pin, HIGH);
    servo.write(SERVO_CTR + controlAngle);
  }

  //------------------------------------------------------------------------------------------------------
  //when lift is desired
  if (lift)
  {

    if (!windSide)
    {
      windAngle = windAngle * -1;
    }

    //if the lift angle isnt enough and the heel angle isnt too much the angle of attack is increased
    if ((MAX_LIFT_ANGLE > windAngle + 1))
    { //&& (abs(heelAngle) <= maxHeelAngle))) {
      if (tabAngle >= 55)
      {
      }
      else
      {
        tabAngle++;
      }
    }

    //if the lift angle is too much or the max heel angle is too much the sail lightens up
    else if ((MAX_LIFT_ANGLE < windAngle))
    { //&& (abs(heelAngle) <= maxHeelAngle)) || (abs(heelAngle) >= maxHeelAngle)) {
      if (tabAngle <= -55)
      {
      }
      else
      {
        tabAngle--;
      }
    }

    //if the angle of attack is correct
    else if (MAX_LIFT_ANGLE == windAngle)
    {
    }

    //to adjust tab angle according to wind side
    if (windSide)
    {
      servo.write(SERVO_CTR + tabAngle);
    }
    else
    {
      servo.write(SERVO_CTR - tabAngle);
    }
  }
  //-----------------------------------------------------------------------------------------------------------
  //while drag if desired
  if (drag)
  {

    //set sail to most possible angle of attack with respect to direction of wind
    if (windSide)
    {
      servo.write(SERVO_CTR + 55);
    }
    else if (!windSide)
    {
      servo.write(SERVO_CTR - 55);
    }
  }
  //----------------------------------------------------------------------------------
  //minimum lift (weathervane)
  if (!lift && !drag && !control)
  {
    digitalWrite(led1Pin, LOW);
    digitalWrite(led2Pin, LOW);

    servo.write(SERVO_CTR);
  }
}
