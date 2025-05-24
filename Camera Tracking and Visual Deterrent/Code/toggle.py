import RPi.GPIO as GPIO
import time

# Use BCM numbering (GPIO 26)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

try:
    while True:
        GPIO.output(26, GPIO.HIGH)  # Turn ON
        time.sleep(0.1)            # 100ms
        GPIO.output(26, GPIO.LOW)   # Turn OFF
        time.sleep(0.1)            # 100ms
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    GPIO.cleanup()
