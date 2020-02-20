#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "ArduinoMessages.pb.h"

#include "pins_arduino.h"

// Buffer for wifi messages
volatile char rx_buffer[6];
volatile char tx_buffer[18];
volatile bool tx_ready = false;
volatile bool rx_ready = false;

int rudder_angle = 90;
int ballast_angle = 90;

// PWM values for reading from the RC receiver
volatile int PWM1_value = 10;
volatile int PWM2_value = 20;
volatile int PWM3_value = 30;
volatile int PWM4_value = 40;
volatile int PWM5_value = 50;
volatile int PWM6_value = 60;

//http://www.gammon.com.au/spi
volatile byte posRx;
volatile byte posTx;

void setup() {
  Serial.begin (9600);   // debugging
  // put your setup code here, to run once:
  
  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);
  
  // turn on SPI in slave mode
  SPCR |= _BV(SPE);
  
  // turn on interrupts
  SPCR |= _BV(SPIE);
  
  posRx = 0;
  rx_ready = false;
}

// SPI interrupt routine
ISR (SPI_STC_vect)
{
byte c = SPDR;
 
 // add to buffer if room
 if (posRx < sizeof rx_buffer)
 {
   rx_buffer [posRx++] = c;
   
   // example: newline means time to process buffer
   if (c == '\n')
     rx_ready = true;
 }  // end of room available

 if(tx_ready){
  SPDR = tx_buffer[posTx];
  posTx--;
  if(posTx ==0){
    tx_ready = false;
  }
 }
}

// main loop - wait for flag set in interrupt routine
void loop (void)
{
 if (rx_ready)
 {
   rx_buffer [posRx] = 0;  
   readProtobuf();
   posRx = 0;
   rx_ready = false;
 }  // end of flag set
 if(!tx_ready){
  writeProtobuf();
 }
}  // end of loop


void readProtobuf(){
  // Prepare a struct to save the message to
  ControlAngles controlAngles = ControlAngles_init_zero;

  // Decode the message and save to a struct
  pb_istream_t stream_rx = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
  bool status_rx = pb_decode(&stream_rx, ControlAngles_fields, &controlAngles);

  Serial.print("Rudder angle: ");
  Serial.print(controlAngles.rudder_angle);
  Serial.print("  Ballast angle: ");
  Serial.println(controlAngles.ballast_angle);

  // Couldn't decode the message, so want to reconnect
  if (!status_rx)
  {
    // Nothing read, so nothing to do
    Serial.println("Couldn't decode!");
    //return;
  }
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
    tx_ready = true;
    posTx = message_length;
  }
}
