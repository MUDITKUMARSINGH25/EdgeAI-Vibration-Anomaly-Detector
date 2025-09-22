# Edge AI for Real-Time Vibration Anomaly Detection (Google Colab)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Colab](https://img.shields.io/badge/Platform-Google%20Colab-orange) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview
This project implements a lightweight, real-time anomaly detection system for vibration sensor data, simulating an Arduino environment. The system is designed for predictive maintenance on industrial equipment.

## Google Colab Notebook
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/EdgeAI-Vibration-Anomaly-Detection/blob/main/Vibration_Anomaly_Detection.ipynb)

Click the button above to open the notebook in Google Colab and run the simulation immediately!

## How It Works
1. **Data Simulation**: Generates realistic vibration sensor data with configurable parameters
2. **Model Training**: Establishes a baseline for normal vibration patterns
3. **Real-time Detection**: Processes data stream-by-stream, detecting anomalies as they occur
4. **Visualization**: Creates comprehensive plots showing the data and detection results

## Theory
The detector uses a moving window to calculate short-term mean (µ) and standard deviation (σ). An anomaly is triggered if the current statistics deviate significantly from the baseline:

`|µ - µ_baseline| > k * σ_baseline` OR `|σ - σ_baseline| > k * σ_baseline`

This approach is computationally efficient, making it ideal for resource-constrained edge devices.

## Results
The system successfully detects injected anomalies while maintaining a low false-positive rate during normal operation.

![Anomaly Detection Results](https://github.com/MUDITKUMARSINGH25/EdgeAI-Vibration-Anomaly-Detector/blob/main/anomaly_detection_plot.png)

## Future Work
- Port to a real Arduino Nano 33 BLE Sense board
- Extend to a micro-trained Decision Tree using TensorFlow Lite for Microcontrollers
- Develop a companion mobile app for Bluetooth-based alerting

---
**Developed by Mudit Kumar Singh (B.Tech ECE)**
