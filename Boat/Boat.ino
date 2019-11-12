/**
 * @file Boat.ino
 * @author Irina Lavryonova (ilavryonova@wpi.edu)
 * @brief Code running on the Arduino Mega located in the Hull of the boat and acting the control system center
 * @version 0.1
 * @date 2019-11-11
 */
#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Constants.h>

#include "pb.h"
#include "pb_common.h"
#include "pb_encode.h"
#include "pb_decode.h"
#include "comms.pb.h"
#include "Constants.h"

/*TODO:*/
// Comms to movable ballast
// Test hall effect reading - move the reading to HERO board

// Buffer for wifi messages
uint8_t tx_buffer[128];
vessel_state tx_message;

// Ethernet server
EthernetServer server(localPort);

// Initialize hall effect states -> TODO: this should move to the HERO board
bool hallStbd = false;
bool hallPort = false;

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

// Initialize vessel state as weather veining
int state = 0;

// Counter to keep track of missed connection attempts (useful for implementing a WIFI timeout)
int msg_miss_counter = 0;



/**
 * @brief Sets up the Arduino
 * Required method
 */
void setup()
{
  // Set hall effect pins as input -> TODO: these should move to the HERO when it is ready
  pinMode(hallPortPin, INPUT);
  pinMode(hallStbdPin, INPUT);

  // Set PWM pins from RC receiver as inputs with pullup
  pinMode(PWM1Pin, INPUT_PULLUP);
  pinMode(PWM2Pin, INPUT_PULLUP);
  pinMode(PWM3Pin, INPUT_PULLUP);
  pinMode(PWM4Pin, INPUT_PULLUP);
  pinMode(PWM5Pin, INPUT_PULLUP);
  pinMode(PWM6Pin, INPUT_PULLUP);

  // Start serial connection
  Serial.begin(9600);
  //Serial2.begin(9600); // TODO: Hero communication

  while (!Serial) {
    ; /* wait for serial port to connect. Needed for native USB port only */
  }

  // Start up the Ethernet connection
  Ethernet.begin(boatMac, hullIP);

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }

  // Start the server on the Arduino
  server.begin();

  // Print diagnostic information about the server
  if (VERBOSE_BOAT) {
    Serial.print("  Server IP: ");
    Serial.print(Ethernet.localIP());
    Serial.print("  Comm port: ");
    Serial.println(localPort);
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
  // All we care about for now is updating the vessel state based on the RC receiver input
  update_vessel_state();
  // TODO: this should eventually go onto the HERO board
  read_hall_effect();
  // TODO: read info from AirMar and update the state accordingly
}


/**
 * @brief Updates the vessel state and publishes to the server
 * 
 * @TODO: make a browser friendly version of the variables
 * @TODO: post updates only when there are changes
 * @TODO: expect a response
 */
void update_vessel_state()
{
  // Check if a client is connected
  EthernetClient client = server.available();
  // Check that the connected client is the trim tab (if not, the connection is poor, since that is the only device that should be connected)
  if (client.remoteIP() == rigidIP) {
    // Fill out msg struct
    tx_message = vessel_state_init_zero;
    tx_message.device_id = DEVICE_ID_ARDUINO;
    tx_message.state = get_state(PWM1_value, PWM6_value);
    tx_message.curHeelAngle = 80;
    tx_message.maxHeelAngle = 30;
    tx_message.controlAngle = map(PWM5_value, 988, 2005, 200, 380); // Read from controller receiver
    tx_message.windAngle = 10;                                      // This is immutable from this side
    tx_message.vIn = 33;                                            // This is immutable from this side
    tx_message.hallPortTrip = hallPort;
    tx_message.hallStbdTrip = hallStbd;

    // Encode message into probuf
    pb_ostream_t stream_tx = pb_ostream_from_buffer(tx_buffer, sizeof(tx_buffer));
    bool status = pb_encode(&stream_tx, vessel_state_fields, &tx_message);

    // Check if message failed to encode, and stop if it did
    if (!status) {
      if(VERBOSE_BOAT) {Serial.println("Failed to encode");}
      return;
    }

    // Successful message transfer, so reset the connecting counter
    msg_miss_counter = 0; 

    // Write protobuf message to server queue
    server.write(tx_buffer, stream_tx.bytes_written);
    //Print diagnostic information
    if (VERBOSE_BOAT) {printPacket(tx_message);}

    // Delay before next message is encoded and sent to make sure that we don't flood the queue and the Teensy has a chance to read what we sent
    delay(20);
  } else {
    if(VERBOSE_BOAT){Serial.println("Unknown connection!");}
    msg_miss_counter++;

    if (msg_miss_counter > 1000) {
      if(VERBOSE_BOAT){Serial.println("Missed too many messages!");}
      // Reset Ethernet board
      Ethernet.begin(boatMac, hullIP);

      // Check for Ethernet hardware present
      if (Ethernet.hardwareStatus() == EthernetNoHardware) {
        Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
        while (true) {
          delay(1); // do nothing, no point running without Ethernet hardware
        }
      }
      server.begin();
      msg_miss_counter = 0;
    }
  }
}



/**
 * @brief Updates the desired state of the boat based on the RC receiver input
 * 
 * @param state1_pwm PWM value of the first switch on the controller
 * @param state2_pwm PWM vlaue of the second switch on the controller
 * @return _TRIM_STATE Enum value corresponding to the desired state of the boat
 */
_TRIM_STATE get_state(int state1_pwm, int state2_pwm)
{
  // Defined using the protobuf header
  // TODO: update so that the states make sense for a sailor
  _TRIM_STATE state = TRIM_STATE_MIN_LIFT;

  if (state1_pwm > 1525) { // stbd
    if (state2_pwm > 1500) {
      state = TRIM_STATE_STBD_TACK;
    } else if (state2_pwm < 1500) {
      state = TRIM_STATE_MAX_DRAG_STBD;
    }
  } else if (state1_pwm > 1475 && state1_pwm < 1525) { // special
    if (state2_pwm > 1500) {
      state = TRIM_STATE_MIN_LIFT;
    } else if (state2_pwm < 1500) {
      state = TRIM_STATE_MAN_CTRL;
    }
  } else if (state1_pwm < 1475) { // port
    if (state2_pwm > 1500) {
      state = TRIM_STATE_PORT_TACK;
    } else if (state2_pwm < 1500) {
      state = TRIM_STATE_MAX_DRAG_PORT;
    }
  }

  return state;
}


/**
 * @brief Routine to update hall effect state
 * @TODO: Should move to the HERO board when that is ready
 * 
 */
void read_hall_effect()
{
  hallPort = digitalRead(hallPortPin) == HIGH;
  hallStbd = digitalRead(hallStbdPin) == HIGH;
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