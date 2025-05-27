# 🐧 Humane Honey Badger Deterrent System  
**EEE4113F Final Year Project – Group 1 (2025)**  
University of Cape Town – Department of Electrical Engineering

## 📋 Overview

This repository contains the full implementation of a humane, AI-assisted deterrent system developed to protect endangered African penguins from honey badger predation. The project was completed as part of the EEE4113F Final Year Design course.

The system integrates real-time animal detection, a web-controlled tactile deterrent, and a visual tracking subsystem, all deployed on low-power, field-ready hardware.

---

## 🧠 Subsystems

### 1. Sensing & Identification 
- Passive infrared (PIR) sensors trigger image capture.
- A 5MP IR camera captures images upon motion detection.
- A TensorFlow Lite model classifies the image into:
  - `honey_badger`, `penguin`, `background`, or `other`
- Upon detecting a honey badger, a GPIO pin is triggered to activate deterrents.

### 2. Tactile Deterrent + Web UI 
- Raspberry Pi-controlled solenoid spray mechanism.
- React-based frontend and Flask backend.
- Features:
  - Manual calibration
  - Livestream from Pi camera
  - Log of past deterrents
  - Weather widget for ranger awareness

### 3. Visual Tracking Subsystem
- Pan-tilt servo system controlled by Raspberry Pi.
- Face detection via OpenCV.
- Flashing light deterrent to startle predators.
- Designed to enhance precision and reduce habituation.
