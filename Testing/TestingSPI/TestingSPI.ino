#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "ArduinoMessages.pb.h"

#include "pins_arduino.h"


// Buffer for wifi messages
volatile byte rx_buffer[13];
volatile char tx_buffer[13];
volatile bool tx_ready = false;
volatile bool rx_ready = false;
volatile bool rxing = false;

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
volatile byte posRx = 0;
volatile byte posTx = 0;

// what to do with incoming data
volatile byte command = 0;

//bool debug_print = true;
//const int debug_size = 13;
//volatile byte debug_array[debug_size];
//
//volatile int counter = 0;

void setup (void)
{

  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);

  // turn on SPI in slave mode
  SPCR |= _BV(SPE);

  // turn on interrupts
  SPCR |= _BV(SPIE);

  Serial.begin(115200);
  writeProtobuf();






  // Prepare a struct to save the message to
  ControlAngles controlAngles = ControlAngles_init_zero;
  int inChar[13] = {39, 92, 120, 48, 56, 91, 92, 120, 49, 48, 92, 92, 39};
  //  String inString;
//  const size_t BUF_MAX = 16;
//  char test[BUF_MAX];
  byte test[5];
  //  int testPos = 0;
  char * test_ptr = test;
  bool escape_flag1 = false;
  bool escape_flag2 = false;

  char hex[1];
//
//  for (int i = 1; i < 13 - 1; i++) {
//    //    inString += (char)inChar[i];
//    //      Serial.print(i);
//    //      Serial.println((char)inChar[i]);
//    //      byte_to_str(buff, (uint8_t)inChar[i]);
//    //        test[i] = nibble_to_hex(inChar[i]);
//    //        test[i] = (char)inChar[i];
//
//    if (escape_flag1 && escape_flag2) {
//      extract = convertCharToHex(a)<<4 | convertCharToHex(b);
//      CardNumberByte[i] = extract;
//      escape_flag1 = false;
//      escape_flag2 = false;
//      i += 2;
//    } else {
//      if (inChar[i] == 92 && !escape_flag1) {
//        escape_flag1 = true;
//      } else if (inChar[i] == 92 && escape_flag1) {
//        *++test_ptr = "\\";
//      } else if (inChar[i] == 120) {
//        escape_flag2 = true;
//      } else {
//        *++test_ptr = (char)inChar[i];
//      }
//    }
//  }
//  *++test_ptr = "\0";
//  *test_ptr = 0;
  
//  for (int i = 0; i < 4; i++)
//  {
//    Serial.print("0x");
//    Serial.println(test[i], HEX);
//  }
  //    char test[] = temp;

  //  Serial.println(F(test));
  //  char test[sizeof(inString)];
  //  inString.toCharArray(test, sizeof(inString));
  //  Serial.println(inString);
  //  Serial.println(test);

  //    for(int i = 0; i < 13; i++){
  //      char val[1] = {0};
  //      String(test[i], HEX).toCharArray(val, 1);
  //      Serial.print(c2h(val[0]>>4));
  //      Serial.print(c2h(val[0]));
  //    }
  //
  //  char test[] = "\x08[\x10\\";
  //  Serial.println(test);
  // Decode the message and save to a struct
  pb_istream_t stream_rx = pb_istream_from_buffer(test, sizeof(test));
  bool status_rx = pb_decode(&stream_rx, ControlAngles_fields, &controlAngles);

  // Couldn't decode the message, so want to reconnect
  if (!status_rx)
  {
    // Nothing read, so nothing to do
    Serial.println("Couldn't decode!");
    //return;
  } else {

    Serial.print("Rudder angle: ");
    Serial.print(controlAngles.rudder_angle);
    Serial.print("  Ballast angle: ");
    Serial.println(controlAngles.ballast_angle);
  }



}  // end of setup

char convertCharToHex(char ch)
{
  char returnType;
  switch(ch)
  {
    case '0':
    returnType = 0;
    break;
    case  '1' :
    returnType = 1;
    break;
    case  '2':
    returnType = 2;
    break;
    case  '3':
    returnType = 3;
    break;
    case  '4' :
    returnType = 4;
    break;
    case  '5':
    returnType = 5;
    break;
    case  '6':
    returnType = 6;
    break;
    case  '7':
    returnType = 7;
    break;
    case  '8':
    returnType = 8;
    break;
    case  '9':
    returnType = 9;
    break;
    case  'A':
    returnType = 10;
    break;
    case  'B':
    returnType = 11;
    break;
    case  'C':
    returnType = 12;
    break;
    case  'D':
    returnType = 13;
    break;
    case  'E':
    returnType = 14;
    break;
    case  'F' :
    returnType = 15;
    break;
    default:
    returnType = 0;
    break;
  }
  return returnType;
}


// SPI interrupt routine
ISR (SPI_STC_vect)
{
  byte c = SPDR;
  SPDR = c;
//  if (c == 39 && !rx_ready) {
//    rxing = true;
//    posRx = 0;
//  }
//  if (rxing) {
//    rx_buffer[posRx] = c;
//    posRx++;
//  }
//  if (c == 39 && rxing) {
//    rxing = false;
//    rx_ready = true;
//  }
//
//
//  if (tx_ready) {
//    if (posTx > -1) {
//      SPDR = tx_buffer[posTx];
//      posTx--;
//      if (posTx == -1) {
//        tx_ready = false;
//      }
//    }
//  }
}  // end of interrupt service routine (ISR) SPI_STC_vect

void loop (void)
{
  //  if (counter == debug_size && debug_print) {
  //    debug_print = false;
  //    for (int i = 0; i < counter; i ++) {
  //      Serial.println(debug_array[i]);
  //    }
  //  }
  if (rx_ready) {
    readProtobuf();
    rx_ready = false;
  }
  if (!tx_ready) {
    writeProtobuf();
  }

}  // end of loop

void bin2SPI() {

}

void SPI2bin() {

}

void readProtobuf() {
  // Prepare a struct to save the message to
  ControlAngles controlAngles = ControlAngles_init_zero;

  // Decode the message and save to a struct
  pb_istream_t stream_rx = pb_istream_from_buffer(rx_buffer, sizeof(rx_buffer));
  bool status_rx = pb_decode(&stream_rx, ControlAngles_fields, &controlAngles);

  // Couldn't decode the message, so want to reconnect
  if (!status_rx)
  {
    // Nothing read, so nothing to do
    Serial.println("Couldn't decode!");
    //return;
  } else {

    Serial.print("Rudder angle: ");
    Serial.print(controlAngles.rudder_angle);
    Serial.print("  Ballast angle: ");
    Serial.println(controlAngles.ballast_angle);
  }
}



void writeProtobuf()
{
  ControlAngles pwm_values = ControlAngles_init_zero;
  size_t message_length;

  // Create a stream that will write to the buffer
  pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));

  // Fill out msg struct
  pwm_values.rudder_angle = PWM1_value;
  pwm_values.ballast_angle = PWM2_value;

  // Encode the message
  bool status_tx = pb_encode(&stream_tx, ControlAngles_fields, &pwm_values);
  message_length = stream_tx.bytes_written;
  Serial.print("TX Message length: ");
  Serial.println(message_length);

  // Check if message failed to encode, and stop if it did
  if (!status_tx) {
    printf("Encoding failed: %s\n", PB_GET_ERROR(&stream_tx));
    return;
  }

  // Write protobuf message to server queue
  if (message_length > 0) {
    tx_ready = true;
    posTx = message_length;
  }
}


//void writeProtobuf()
//{
//  PWMValues pwm_values = PWMValues_init_zero;
//  size_t message_length;
//
//  // Create a stream that will write to the buffer
//  pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
//
//  // Fill out msg struct
//  pwm_values.ch1 = PWM1_value;
//  pwm_values.ch2 = PWM2_value;
//  pwm_values.ch3 = PWM3_value;
//  pwm_values.ch4 = PWM4_value;
//  pwm_values.ch5 = PWM5_value;
//  pwm_values.ch6 = PWM6_value;
//
//  // Encode the message
//  bool status_tx = pb_encode(&stream_tx, PWMValues_fields, &pwm_values);
//  message_length = stream_tx.bytes_written;
//  Serial.print("TX Message length: ");
//  Serial.println(message_length);
//
//  // Check if message failed to encode, and stop if it did
//  if (!status_tx) {
//    printf("Encoding failed: %s\n", PB_GET_ERROR(&stream_tx));
//    return;
//  }
//
//  // Write protobuf message to server queue
//  if (message_length > 0) {
//    tx_ready = true;
//    posTx = message_length;
//  }
//}
