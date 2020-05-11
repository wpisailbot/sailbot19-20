# Arduino
The Arduino is necessary to read the PWM output from the RC receiver used for teleoperation. This is because the BBB does not have a sufficient number of PWM inputs and an adequate work around could not be found. There may be a better method of reading PWM signals using the BBB and it should be implemented in order to simplify the system.

# Deploying code
Using the Arduino IDE, locate the board and deploy code. This code is intended to be run on an Arduino Mega, but it can also be run on another version of Arduino for testing if necesarry.

If deploying to an Arduino Uno, which only has one serial port, be sure to unplug the UART cables before deploying and changing the code to use Serial instead of Serial1.

# Using with the BBB
Check the pin allocations in the report for the pins used in this code and attach the appropriate pins to the BBB and the Arduino. Note that for UART to work, the UART lines of the two boards must be crossed such that RX of one board goes to the TX of the other board and vice versa.

The companion code for this board is PWM_IO.py for operation and UART_test.py for testing.