import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
relay_pin = 18

# Set the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)

# Turn on the relay for 5 seconds
GPIO.output(relay_pin, GPIO.HIGH)
time.sleep(10)

# Turn off the relay
GPIO.output(relay_pin, GPIO.LOW)

# Clean up the GPIO pins
GPIO.cleanup()
