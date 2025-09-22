#!/usr/bin/env python3
"""
Generates plots to visualize the simulated data and anomaly detection results.
"""

import numpy as np
import matplotlib.pyplot as plt
import json

# Generate the sample data with an anomaly
from data_simulator import generate_vibration_data
from anomaly_detector import AnomalyDetector

# Load the trained model
try:
    with open('../models/baseline_params.json', 'r') as f:
        params = json.load(f)
    detector = AnomalyDetector()
    detector.baseline_mean = params['baseline_mean']
    detector.baseline_std = params['baseline_std']
    detector.threshold = params['threshold']
except FileNotFoundError:
    print("Model not found. Please train the model first.")
    exit()

# Generate test data
data = generate_vibration_data()
anomaly_flags = []
means = []
stds = []

window_size = 10
# Simulate processing the data in a rolling window
for i in range(len(data) - window_size):
    window = data[i:i+window_size]
    is_anomaly, current_mean, current_std = detector.check_anomaly(window)
    anomaly_flags.append(is_anomaly)
    means.append(current_mean)
    stds.append(current_std)

# Pad the lists to match the original data length for plotting
anomaly_flags = [False] * (window_size // 2) + anomaly_flags + [False] * (window_size // 2)
means = [np.mean(data[:window_size])] * (window_size // 2) + means + [means[-1]] * (window_size // 2)
stds = [np.std(data[:window_size])] * (window_size // 2) + stds + [stds[-1]] * (window_size // 2)

# Create the plot
plt.figure(figsize=(12, 8))

# Plot the raw data
plt.subplot(3, 1, 1)
plt.plot(data, 'b-', label='Vibration Signal', alpha=0.7)
plt.title('Simulated Vibration Sensor Data with Anomaly')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot the moving statistics
plt.subplot(3, 1, 2)
plt.plot(means, 'g-', label='Moving Mean', linewidth=2)
plt.axhline(y=detector.baseline_mean, color='k', linestyle='--', label='Baseline Mean')
plt.fill_between(range(len(data)), detector.baseline_mean - detector.threshold*detector.baseline_std,
                 detector.baseline_mean + detector.threshold*detector.baseline_std, color='gray', alpha=0.2, label='Normal Range')
plt.ylabel('Mean Value')
plt.legend()
plt.grid(True)

# Plot the anomaly flags
plt.subplot(3, 1, 3)
anomaly_indices = np.where(anomaly_flags)[0]
plt.plot(anomaly_indices, [1] * len(anomaly_indices), 'ro', label='Detected Anomaly', markersize=4)
plt.title('Anomaly Detection Results')
plt.xlabel('Sample Index')
plt.yticks([0, 1], ['Normal', 'Anomaly'])
plt.ylim(-0.5, 1.5)
plt.legend(loc='upper right')
plt.grid(True)

plt.tight_layout()
plt.savefig('../anomaly_detection_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'anomaly_detection_plot.png'")
# plt.show() # Uncomment this if you want to see the plot immediately
