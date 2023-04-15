import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# Set the GPIO mode and pin number
GPIO.setmode(GPIO.BCM)
relay_pin = 21 #12 pin

# Set the GPIO pin as an output
GPIO.setup(relay_pin, GPIO.OUT)

while True:
    # Turn on the relay for 5 seconds
    GPIO.output(relay_pin, GPIO.HIGH)
    print("ON")
    time.sleep(1)

    # Turn off the relay
    GPIO.output(relay_pin, GPIO.LOW)
    print("OFF")
    time.sleep(1)

# Clean up the GPIO pins
GPIO.cleanup()
