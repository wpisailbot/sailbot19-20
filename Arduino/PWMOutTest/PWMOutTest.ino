int PWM_pin = 10;

void setup()
{
    pinMode(PWM_pin, OUTPUT);
}

void loop()
{
    analogWrite(PWM_pin, 127);
}