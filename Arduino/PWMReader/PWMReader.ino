/**
 * @file PWMReader.ino
 * @author Irina Lavryonova (ilavryonova@wpi.edu)
 * @brief Code running on the Arduino Mega located in the Hull of the boat reading PWM values.
 * @version 0.5
 * @date 2020-03-10
 */
#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "PWMMessages.pb.h"

// Buffer for wifi messages
uint8_t tx_buffer[128];
PWMValues tx_message;

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


/**
 * @brief Sets up the Arduino
 * Required method
 */
void setup()
{
  // Set PWM pins from RC receiver as inputs with pullup
  pinMode(PWM1Pin, INPUT_PULLUP);
  pinMode(PWM2Pin, INPUT_PULLUP);
  pinMode(PWM3Pin, INPUT_PULLUP);
  pinMode(PWM4Pin, INPUT_PULLUP);
  pinMode(PWM5Pin, INPUT_PULLUP);
  pinMode(PWM6Pin, INPUT_PULLUP);

  // Start serial connection
  Serial.begin(9600); // Debug output
  Serial1.begin(115200); // BBB communication - make sure baud here and in PWM_IO match!!

  while (!Serial) {
    ; /* wait for serial port to connect. Needed for native USB port only */
  }
  
  // Attach RC receiver PWM pins to interrupts so that we are not blocking code when reading from the receiver and not missing edges
  attachInterrupt(PWM1Pin, rising_PWM1, RISING);
  attachInterrupt(PWM2Pin, rising_PWM2, RISING);
  attachInterrupt(PWM3Pin, rising_PWM3, RISING);
  attachInterrupt(PWM4Pin, rising_PWM4, RISING);
  attachInterrupt(PWM5Pin, rising_PWM5, RISING);
  attachInterrupt(PWM6Pin, rising_PWM6, RISING);
}



/**
 * @brief Everything in this method gets called repeatedly
 * Required method
 */
void loop()
{
  packAndSendMessage()
}


/**
 * @brief Updates the vessel state and sends to BBB via UART
 * This is one way communcation, so no responce is expected from the BBB.
 */
void packAndSendMessage()
{
  // Fill out msg struct
  tx_message = PWMValues_init_zero;
  tx_message.ch1 = PWM1_value;
  tx_message.ch2 = PWM2_value;
  tx_message.ch3 = PWM3_value;
  tx_message.ch4 = PWM4_value;
  tx_message.ch5 = PWM5_value;
  tx_message.ch6 = PWM6_value;
  
  // Encode message into protobuf
  pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
  bool status = pb_encode(&stream_tx, vessel_state_fields, &tx_message);

  // Check if message failed to encode, and stop if it did
  if (!status) {
    if(VERBOSE_BOAT) {Serial.println("Failed to encode");}
    return;
  }

  // Write protobuf message to server queue
  Serial1.write(tx_buffer, stream_tx.bytes_written);
  delay(100); // Tell BBB that we're done sending this message
}


/**
 * This is using the interrupts to time the edges of the PWM pulses. This returns the duty cycle time and thus is not a ratio of the period.
 */
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
