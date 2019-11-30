/*
 Analog input reads an analog input on analog in 0, prints the value out.
 created 24 March 2006
 by Tom Igoe
 */

int analogValue = 0;    // variable to hold the analog value

void setup() {
  // open the serial port at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  Serial.println("Hi, I'm Arduino!");       // print as an ASCII-encoded decimal
  delay(10);
}
