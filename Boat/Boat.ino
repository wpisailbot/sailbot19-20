#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "test.pb.h"
#include "Constants.h"


/*TODO*/
// CAN to movable ballast

uint8_t tx_buffer[128];
vehicle_state tx_message;

EthernetServer server(localPort);

int hallStbd = LOW;
int hallPort = LOW;


volatile int PWM1_value = 0;
volatile int PWM2_value = 0;
volatile int PWM3_value = 0;
volatile int PWM4_value = 0;
volatile int PWM5_value = 0;
volatile int PWM6_value = 0;


volatile int PWM1_prev_time = 0;
volatile int PWM2_prev_time = 0;
volatile int PWM3_prev_time = 0;
volatile int PWM4_prev_time = 0;
volatile int PWM5_prev_time = 0;
volatile int PWM6_prev_time = 0;

int state = 0;

void setup() {
  pinMode(hallPortPin, INPUT);
  pinMode(hallStbdPin, INPUT);
  pinMode(PWM1Pin, INPUT);
  pinMode(PWM2Pin, INPUT);
  pinMode(PWM3Pin, INPUT);
  pinMode(PWM4Pin, INPUT);
  pinMode(PWM5Pin, INPUT);
  pinMode(PWM6Pin, INPUT);

  Serial.begin(9600);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB port only
  }
  // Set up the server on the arduino
  Ethernet.begin(boatMac, hullIP);

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
      Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
      while (true) {
          delay(1); // do nothing, no point running without Ethernet hardware
      }
  }

  server.begin();

  Serial.print("  Server IP: ");
  Serial.print(Ethernet.localIP());
  Serial.print("  Comm port: ");
  Serial.println(localPort);

  
  attachInterrupt(digitalPinToInterrupt(PWM1Pin), rising_PWM1, RISING);
  attachInterrupt(digitalPinToInterrupt(PWM2Pin), rising_PWM2, RISING);
  attachInterrupt(digitalPinToInterrupt(PWM3Pin), rising_PWM3, RISING);
  attachInterrupt(digitalPinToInterrupt(PWM4Pin), rising_PWM4, RISING);
  attachInterrupt(digitalPinToInterrupt(PWM5Pin), rising_PWM5, RISING);
  attachInterrupt(digitalPinToInterrupt(PWM6Pin), rising_PWM6, RISING);
}

void loop() {
  update_vehicle_state();
  // Read from Serial Terminal for state -- testing only
  if (Serial.available() > 0) {
    // read the incoming byte:
    state = Serial.read() - 48;

    Serial.print("State:");
    Serial.println(state);
  }

  read_hall_effect();
}


void update_vehicle_state()
{
    EthernetClient client = server.available();
    if(!client.connected()){
      //Serial.println("Client disconnected!");
      // Unstick socket
      Ethernet.begin(boatMac, hullIP);
  
      // Check for Ethernet hardware present
      if (Ethernet.hardwareStatus() == EthernetNoHardware) {
          Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
          while (true) {
              delay(1); // do nothing, no point running without Ethernet hardware
          }
      }
  
      server.begin();
  
//      Serial.print("  Server IP: ");
//      Serial.print(Ethernet.localIP());
//      Serial.print("  Comm port: ");
//      Serial.println(localPort);
    }
        tx_message = vehicle_state_init_zero;
        tx_message.state = (_TRIM_STATE)state;
        tx_message.curHeelAngle = 80;
        tx_message.maxHeelAngle = 30;
        tx_message.controlAngle = PWM6_value/PWM_period*360 - 180; // Read from controller receiver
        tx_message.windAngle = 10;    // This is immutable from this side
        tx_message.vIn = 33;          // This is immutable from this side

        // Serial.print("  State:");
        // Serial.print(tx_message.state);
        // Serial.print("  curAngle:");
        // Serial.print(tx_message.curHeelAngle);
        // Serial.print("  maxAngle:");
        // Serial.print(tx_message.maxHeelAngle);
        // Serial.print("  ControlAngle:");
        // Serial.print(tx_message.controlAngle);
        // Serial.print("  WindAngle:");
        // Serial.print(tx_message.windAngle);
        // Serial.print("  vIn:");
        // Serial.print(tx_message.vIn);
        // Serial.println();

        pb_ostream_t stream = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
        bool status = pb_encode(&stream, vehicle_state_fields, &tx_message);
    
        if (!status)
        {
            Serial.println("Failed to encode");
            return;
        }

        server.write(tx_buffer, stream.bytes_written);
}


void read_hall_effect(){
  hallPort = digitalRead(hallPortPin);
  hallStbd = digitalRead(hallStbdPin);
}

void rising_PWM1() {
  attachInterrupt(PWM1Pin, falling_PWM1, FALLING);
  PWM1_prev_time = micros();
}
 
void falling_PWM1() {
  attachInterrupt(PWM1Pin, rising_PWM1, RISING);
  PWM1_value = micros()-PWM1_prev_time;
  Serial.print("  PWM1:");
  Serial.println(PWM1_value);
}

void rising_PWM2() {
  attachInterrupt(PWM2Pin, falling_PWM2, FALLING);
  PWM2_prev_time = micros();
}
 
void falling_PWM2() {
  attachInterrupt(PWM2Pin, rising_PWM2, RISING);
  PWM2_value = micros()-PWM2_prev_time;
  Serial.print("  PWM2:");
  Serial.println(PWM2_value);
}

void rising_PWM3() {
  attachInterrupt(PWM3Pin, falling_PWM3, FALLING);
  PWM3_prev_time = micros();
}
 
void falling_PWM3() {
  attachInterrupt(PWM3Pin, rising_PWM3, RISING);
  PWM3_value = micros()-PWM3_prev_time;
  Serial.print("  PWM3:");
  Serial.println(PWM3_value);
}

void rising_PWM4() {
  attachInterrupt(PWM4Pin, falling_PWM4, FALLING);
  PWM4_prev_time = micros();
}
 
void falling_PWM4() {
  attachInterrupt(PWM4Pin, rising_PWM4, RISING);
  PWM4_value = micros()-PWM4_prev_time;
  Serial.print("  PWM4:");
  Serial.println(PWM4_value);
}

void rising_PWM5() {
  attachInterrupt(PWM5Pin, falling_PWM5, FALLING);
  PWM5_prev_time = micros();
}
 
void falling_PWM5() {
  attachInterrupt(PWM5Pin, rising_PWM5, RISING);
  PWM5_value = micros()-PWM5_prev_time;
  Serial.print("  PWM5:");
  Serial.println(PWM5_value);
}

void rising_PWM6() {
  attachInterrupt(PWM6Pin, falling_PWM6, FALLING);
  PWM6_prev_time = micros();
}
 
void falling_PWM6() {
  attachInterrupt(PWM6Pin, rising_PWM6, RISING);
  PWM6_value = micros()-PWM6_prev_time;
  Serial.print("  PWM6:");
  Serial.println(PWM6_value);
}
