#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "ArduinoMessages.pb.h"

#include "Servo.h"

// Buffer for wifi messages
uint8_t rx_buffer[6];
char tx_buffer[18];

Servo rudderservo;
Servo ballastmotor;

bool readingNow = false;

// PWM values for reading from the RC receiver
volatile int PWM1_value = 0;
volatile int PWM2_value = 0;
volatile int PWM3_value = 0;
volatile int PWM4_value = 0;
volatile int PWM5_value = 0;
volatile int PWM6_value = 0;


// PWM timing values used for reading the PWM dutycycle of the RC receiver
volatile int PWM1_prev_time = 0;
volatile int PWM2_prev_time = 0;
volatile int PWM3_prev_time = 0;
volatile int PWM4_prev_time = 0;
volatile int PWM5_prev_time = 0;
volatile int PWM6_prev_time = 0;


int rudder_angle = 90;
int ballast_angle = 90;

int rudder_accum = 0;
int ballast_accum = 0;
int accum_counter = 0;

void setup()
{
    Serial.begin(9600);
    Serial3.begin(9600);
    
    while (!Serial3) {
    ; /* wait for serial port to connect. Needed for native USB port only */
    }
    
    rudderservo.attach(rudderServoPin);
    ballastmotor.attach(balastMotorPin);
    
    pinMode(PWM1Pin, INPUT_PULLUP);
    pinMode(PWM2Pin, INPUT_PULLUP);
    pinMode(PWM3Pin, INPUT_PULLUP);
    pinMode(PWM4Pin, INPUT_PULLUP);
    pinMode(PWM5Pin, INPUT_PULLUP);
    pinMode(PWM6Pin, INPUT_PULLUP);
    
    // Attach RC receiver PWM pins to interrupts so that we are not blocking code when reading from the receiver and not missing edges
    attachInterrupt(PWM1Pin, rising_PWM1, RISING);
    attachInterrupt(PWM2Pin, rising_PWM2, RISING);
    attachInterrupt(PWM3Pin, rising_PWM3, RISING);
    attachInterrupt(PWM4Pin, rising_PWM4, RISING);
    attachInterrupt(PWM5Pin, rising_PWM5, RISING);
    attachInterrupt(PWM6Pin, rising_PWM6, RISING);

    // Set hall effect pins as input -> TODO: these should move to the HERO when it is ready
    pinMode(hallPortPin, INPUT);
    pinMode(hallStbdPin, INPUT);

    // set the slaveSelectPin as an output:
    pinMode(slaveSelectPin, OUTPUT);
    // initialize SPI:
    SPI.begin();
}

void loop() {
  analogWrite(6, 256/4);
  simpleSendReceive();
}

void simpleSendReceive()
{
  delay(100);
  if(!readingNow){
    writeProtobuf();
    delay(100);
  }
  if(readingNow){
    readProtobuf();
    delay(100);
  }
//  delay(100);
}

void readProtobuf(){
  // If there's data available, read a rx_packet
  int bytes = Serial3.available();
  
  if (bytes){// Read the bytes into a buffer so that we can decode them
//    Serial.print("RX Message length: ");
//    Serial.println(bytes);
    for (int i = 0; i < bytes; i++)
    {
      rx_buffer[i] = (uint8_t)Serial3.read();
    }
  
    // Prepare a struct to save the message to
    ControlAngles controlAngles = ControlAngles_init_zero;
  
    // Decode the message and save to a struct
    pb_istream_t stream_rx = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
    bool status_rx = pb_decode(&stream_rx, ControlAngles_fields, &controlAngles);
  
    // Couldn't decode the message, so want to reconnect
    if (!status_rx)
    {
      // Nothing read, so nothing to do
      Serial3.println("Couldn't decode!");
      //return;
    }
//    float tempRudderAngle = (controlAngles.rudder_angle-980)*PWMScaler;
//    float tempBallastAngle = (controlAngles.ballast_angle-980)*PWMScaler;
    float tempRudderAngle = (PWM2_value-980)*PWMScaler;
    float tempBallastAngle = (PWM3_value-980)*PWMScaler;
    float rudderDiff = abs(rudder_angle - tempRudderAngle);
    float ballastDiff = abs(ballast_angle - tempBallastAngle);
    rudder_angle = tempRudderAngle >= 0  && tempRudderAngle <= 180  && rudderDiff < 90? tempRudderAngle : rudder_angle;
//    rudder_angle = tempRudderAngle < 181 ? tempRudderAngle : rudder_angle;
    ballast_angle = tempBallastAngle >= 0  && tempBallastAngle <= 180 && ballastDiff < 90? tempBallastAngle : ballast_angle;
//    ballast_angle = tempBallastAngle > 0 ? tempBallastAngle : ballast_angle;
//    ballast_angle = tempBallastAngle < 181 ? tempBallastAngle : ballast_angle;

    Serial.print("Rudder angle: ");
    Serial.print(rudder_angle);
    Serial.print("  Ballast angle: ");
    Serial.println(ballast_angle);

    
    rudderservo.write(rudder_angle);
    delay(100);
    ballastmotor.write(ballast_angle);
    delay(100);

//    if(accum_counter < 10){
//      rudder_accum += rudder_angle;
//      ballast_accum += ballast_angle;
//      accum_counter++;
//    } else {
//      rudderservo.write(rudder_accum/10);
//      ballastmotor.write(ballast_accum/10);
//      accum_counter = 0;
//      rudder_accum = 0;
//      ballast_accum = 0;
//    }
  }
  readingNow = false;
}

void writeProtobuf()
{
  PWMValues pwm_values = PWMValues_init_zero;
  size_t message_length;
  
  // Create a stream that will write to the buffer
  pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
  
  // Fill out msg struct
  pwm_values.ch1 = PWM1_value;
  pwm_values.ch2 = PWM2_value;
  pwm_values.ch3 = PWM3_value;
  pwm_values.ch4 = PWM4_value;
  pwm_values.ch5 = PWM5_value;
  pwm_values.ch6 = PWM6_value;

//  Serial.print("PWM1_value: ");
//  Serial.print(pwm_values.ch1);
//  Serial.print("  PWM2_value: ");
//  Serial.print(pwm_values.ch2);
//  Serial.print("  PWM3_value: ");
//  Serial.print(pwm_values.ch3);
//  Serial.print("  PWM4_value: ");
//  Serial.print(pwm_values.ch4);
//  Serial.print("  PWM5_value: ");
//  Serial.print(pwm_values.ch5);
//  Serial.print("  PWM6_value: ");
//  Serial.println(pwm_values.ch6);

  // Encode the message
  bool status_tx = pb_encode(&stream_tx, PWMValues_fields, &pwm_values);
  message_length = stream_tx.bytes_written;
//  Serial.print("TX Message length: ");
//  Serial.println(message_length);

  // Check if message failed to encode, and stop if it did
  if (!status_tx) {
    printf("Encoding failed: %s\n", PB_GET_ERROR(&stream_tx));
    return;
  }
  
  // Write protobuf message to server queue
  if(message_length > 0){
    size_t written = Serial3.write(tx_buffer, message_length);
    Serial3.flush();
    if(written){
      readingNow = true;
    }
  }
}


/******************* START PWM INTERRUPT ROUTINES ****************************/
void rising_PWM1()
{
  attachInterrupt(PWM1Pin, falling_PWM1, FALLING);
  PWM1_prev_time = micros();
}

void falling_PWM1()
{
  attachInterrupt(PWM1Pin, rising_PWM1, RISING);
  PWM1_value = micros() - PWM1_prev_time;
}

void rising_PWM2()
{
  attachInterrupt(PWM2Pin, falling_PWM2, FALLING);
  PWM2_prev_time = micros();
}

void falling_PWM2()
{
  attachInterrupt(PWM2Pin, rising_PWM2, RISING);
  PWM2_value = micros() - PWM2_prev_time;
}

void rising_PWM3()
{
  attachInterrupt(PWM3Pin, falling_PWM3, FALLING);
  PWM3_prev_time = micros();
}

void falling_PWM3()
{
  attachInterrupt(PWM3Pin, rising_PWM3, RISING);
  PWM3_value = micros() - PWM3_prev_time;
}

void rising_PWM4()
{
  attachInterrupt(PWM4Pin, falling_PWM4, FALLING);
  PWM4_prev_time = micros();
}

void falling_PWM4()
{
  attachInterrupt(PWM4Pin, rising_PWM4, RISING);
  PWM4_value = micros() - PWM4_prev_time;
}

void rising_PWM5()
{
  attachInterrupt(PWM5Pin, falling_PWM5, FALLING);
  PWM5_prev_time = micros();
}

void falling_PWM5()
{
  attachInterrupt(PWM5Pin, rising_PWM5, RISING);
  PWM5_value = micros() - PWM5_prev_time;
}

void rising_PWM6()
{
  attachInterrupt(PWM6Pin, falling_PWM6, FALLING);
  PWM6_prev_time = micros();
}

void falling_PWM6()
{
  attachInterrupt(PWM6Pin, rising_PWM6, RISING);
  PWM6_value = micros() - PWM6_prev_time;
}
/******************* END PWM INTERRUPT ROUTINES ****************************/
