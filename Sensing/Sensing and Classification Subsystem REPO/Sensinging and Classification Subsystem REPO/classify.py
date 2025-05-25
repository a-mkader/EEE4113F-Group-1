import time
import os
from datetime import datetime
import numpy as np
from picamera import PiCamera
import RPi.GPIO as GPIO
from tflite_support.task import core, vision

# === CONFIGURATION ===
PIR_PIN = 14       # PIR input GPIO
OUT_PIN = 17       # GPIO output (e.g., trigger deterrent)
MODEL_PATH = "model.tflite"  # TFLite model file
THRESHOLD = 0.6    # Confidence threshold to trigger

# === SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(OUT_PIN, GPIO.OUT)
GPIO.output(OUT_PIN, GPIO.LOW)

camera = PiCamera()
camera.resolution = (224, 224)  # Match input size of model
time.sleep(2)

image_dir = "images"
os.makedirs(image_dir, exist_ok=True)

# === LOAD MODEL ===
base_options = core.BaseOptions(file_name=MODEL_PATH)
options = vision.ImageClassifierOptions(base_options=base_options)
classifier = vision.ImageClassifier.create_from_options(options)

def capture_image():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(image_dir, f"classify_{timestamp}.jpg")
    camera.capture(image_path)
    return image_path

def classify_image(image_path):
    img = vision.TensorImage.create_from_file(image_path)
    result = classifier.classify(img)
    if result.classifications:
        top_result = result.classifications[0].categories[0]
        label, score = top_result.category_name, top_result.score
        print(f"Prediction: {label} ({score:.2f})")
        return label, score
    return None, 0.0

print("Classifier ready. Waiting for PIR trigger...")

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected.")
            image_path = capture_image()
            label, confidence = classify_image(image_path)

            if label.lower() == "honey_badger" and confidence >= THRESHOLD:
                print("Honey badger detected! Triggering deterrent...")
                GPIO.output(OUT_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(OUT_PIN, GPIO.LOW)
            else:
                print("No honey badger. No action taken.")

            time.sleep(2)  # Avoid multiple classifications
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    camera.close()
    GPIO.cleanup()
