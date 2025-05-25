import time
from picamera import PiCamera
import RPi.GPIO as GPIO
from datetime import datetime
import os

# GPIO setup
PIR_PIN = 14  # Adjust if different
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Initialize camera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
time.sleep(2)  # Let camera adjust to lighting

# Image directory setup
image_dir = "images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

print("PIR sensor active. Waiting for motion...")

try:
    while True:
        if GPIO.input(PIR_PIN):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image_path = os.path.join(image_dir, f"capture_{timestamp}.jpg")
            print(f"Motion detected! Capturing image: {image_path}")
            camera.capture(image_path)
            time.sleep(2)  # Avoid multiple captures per detection
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting capture script...")
finally:
    camera.close()
    GPIO.cleanup()
