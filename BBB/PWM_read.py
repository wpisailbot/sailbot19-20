import Adafruit_BBIO.GPIO as GPIO
import Constants as CONST
import time
import logger as LOG

class PWM_Reader:
    """
    Reads PWM values from the RC receiver.
    The basic idea is to time the time between rising and falling edges.
    Using ISRs here because we don't want to miss any edges.
    """

    def __init__(self):
        self.__state1_pwm_val = 0
        self.__state2_pwm_val = 0
        self.__ballas_pwm_val = 0
        self.__rudder_pwm_val = 0
        self.__manctr_pwm_val = 0
        self.__unused_pwm_val = 0
        self.__state1_pwm_prev_time = 0
        self.__state2_pwm_prev_time = 0
        self.__ballas_pwm_prev_time = 0
        self.__rudder_pwm_prev_time = 0
        self.__manctr_pwm_prev_time = 0
        self.__unused_pwm_prev_time = 0

        GPIO.setup(CONST.STATE1_PIN, GPIO.IN)
        GPIO.setup(CONST.STATE2_PIN, GPIO.IN)
        GPIO.setup(CONST.BALLAS_PIN, GPIO.IN)
        GPIO.setup(CONST.RUDDER_PIN, GPIO.IN)
        GPIO.setup(CONST.MANCTR_PIN, GPIO.IN)
        GPIO.setup(CONST.UNUSED_PIN, GPIO.IN)

        GPIO.add_event_detect(CONST.STATE1_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)
        GPIO.add_event_detect(CONST.STATE2_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)
        GPIO.add_event_detect(CONST.BALLAS_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)
        GPIO.add_event_detect(CONST.RUDDER_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)
        GPIO.add_event_detect(CONST.MANCTR_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)
        GPIO.add_event_detect(CONST.UNUSED_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)

        LOG.LOG_I("PWM reader is ready!")

    ### -------------------------- GETTERS START -------------------------- ###
    def get_state1_val(self):
        return self.__state1_pwm_val

    def get_state2_val(self):
        return self.__state2_pwm_val

    def get_ballas_val(self):
        return self.__ballas_pwm_val

    def get_rudder_val(self):
        return self.__rudder_pwm_val

    def get_manctr_val(self):
        return self.__manctr_pwm_val

    def get_state1_val(self):
        return self.__state1_pwm_val
    ### -------------------------- GETTERS END -------------------------- ###
    

    def cleanup(self):
        GPIO.cleanup()

    ### -------------------------- ISRs START -------------------------- ###
    def __STATE1_RISING_ISR(self, channel):
        if GPIO.input(CONST.STATE1_PIN):
            self.__state1_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.STATE1_PIN, GPIO.FALLING, self.__STATE1_FALLING_ISR)

    def __STATE1_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.STATE1_PIN):
            self.__state1_pwm_val = self.__state1_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.STATE1_PIN, GPIO.RISING, self.__STATE1_RISING_ISR)

    def __STATE2_RISING_ISR(self, channel):
        if GPIO.input(CONST.STATE2_PIN):
            self.__state2_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.STATE2_PIN, GPIO.FALLING, self.__STATE2_FALLING_ISR)

    def __STATE2_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.STATE2_PIN):
            self.__state2_pwm_val = self.__state2_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.STATE2_PIN, GPIO.RISING, self.__STATE2_RISING_ISR)

    def __BALLAS_RISING_ISR(self, channel):
        if GPIO.input(CONST.BALLAS_PIN):
            self.__ballas_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.BALLAS_PIN, GPIO.FALLING, self.__BALLAS_FALLING_ISR)

    def __BALLAS_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.BALLAS_PIN):
            self.__ballas_pwm_val = self.__ballas_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.BALLAS_PIN, GPIO.RISING, self.__BALLAS_RISING_ISR)

    def __RUDDER_RISING_ISR(self, channel):
        if GPIO.input(CONST.RUDDER_PIN):
            self.__rudder_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.RUDDER_PIN, GPIO.FALLING, self.__RUDDER_FALLING_ISR)

    def __RUDDER_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.RUDDER_PIN):
            self.__rudder_pwm_val = self.__rudder_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.RUDDER_PIN, GPIO.RISING, self.__RUDDER_RISING_ISR)

    def __MANCTR_RISING_ISR(self, channel):
        if GPIO.input(CONST.MANCTR_PIN):
            self.__manctr_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.MANCTR_PIN, GPIO.FALLING, self.__MANCTR_FALLING_ISR)

    def __MANCTR_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.MANCTR_PIN):
            self.__manctr_pwm_val = self.__manctr_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.MANCTR_PIN, GPIO.RISING, self.__MANCTR_RISING_ISR)

    def __UNUSED_RISING_ISR(self, channel):
        if GPIO.input(CONST.UNUSED_PIN):
            self.__unused_pwm_prev_time = time.time()
            GPIO.add_event_detect(CONST.UNUSED_PIN, GPIO.FALLING, self.__UNUSED_FALLING_ISR)

    def __UNUSED_FALLING_ISR(self, channel):
        if not GPIO.input(CONST.UNUSED_PIN):
            self.__unused_pwm_val = self.__unused_pwm_prev_time - time.time()
            GPIO.add_event_detect(CONST.UNUSED_PIN, GPIO.RISING, self.__UNUSED_RISING_ISR)
    ### -------------------------- ISRs END -------------------------- ###