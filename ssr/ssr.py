import RPi.GPIO as GPIO
import time


class SSR:

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin

    def get_state(self):
        return GPIO.input(self.pin)

    state = property(get_state)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

