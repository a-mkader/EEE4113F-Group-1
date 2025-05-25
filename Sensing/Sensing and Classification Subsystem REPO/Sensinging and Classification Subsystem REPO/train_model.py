import os
from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader
import tensorflow as tf

# === CONFIGURATION ===
DATA_DIR = "animal_dataset"
MODEL_OUTPUT = "model.tflite"
IMG_SIZE = 224
EPOCHS = 15
BATCH_SIZE = 16

# === LOAD DATA ===
print("Loading dataset...")
data = DataLoader.from_folder(DATA_DIR)
train_data, test_data = data.split(0.8)

# === MODEL TRAINING ===
print("Training model...")
model = image_classifier.create(
    train_data=train_data,
    model_spec=image_classifier.ModelSpec.MOBILENET_V2,
    validation_data=test_data,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE
)

# === EVALUATION ===
print("Evaluating model...")
loss, accuracy = model.evaluate(test_data)
print(f"Validation accuracy: {accuracy:.2f}")

# === EXPORT MODEL ===
print(f"Saving TFLite model to {MODEL_OUTPUT}...")
model.export(export_format="TFLITE", filename=MODEL_OUTPUT)
model.summary()
