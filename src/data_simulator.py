#!/usr/bin/env python3
"""
Simulates an Arduino streaming vibration sensor data.
Generates a realistic signal with optional anomalies for training and testing.
"""

import numpy as np
import argparse
import time
import csv

def generate_vibration_data(length=1000, frequency=5.0, noise_level=0.2, include_anomaly=True, anomaly_start=700, anomaly_length=100):
    """
    Generates a realistic vibration sensor signal.
    """
    time_vec = np.linspace(0, 10, length)
    # Base signal: a simple sine wave representing normal vibration
    base_signal = np.sin(2 * np.pi * frequency * time_vec)

    # Add some random noise (always present in real sensors)
    noise = noise_level * np.random.randn(length)
    signal = base_signal + noise

    # Simulate a potential fault (a sudden change in amplitude and frequency)
    if include_anomaly:
        anomaly_slice = slice(anomaly_start, anomaly_start + anomaly_length)
        signal[anomaly_slice] = 2.0 * np.sin(2 * np.pi * 15.0 * time_vec[anomaly_slice]) + 0.5 * np.random.randn(anomaly_length)

    return signal

def stream_data(signal, delay=0.1):
    """
    Mimics an Arduino streaming data one value at a time.
    """
    for i, value in enumerate(signal):
        print(f"Sample {i}: {value:.4f}", end=' - ') # Simulate printing to Serial
        yield i, value
        time.sleep(delay) # Simulate delay between readings

def main():
    parser = argparse.ArgumentParser(description='Vibration Sensor Data Simulator')
    parser.add_argument('--generate_training_data', action='store_true', help='Generate a clean dataset for training')
    args = parser.parse_args()

    # Generate the main signal with an anomaly for demonstration
    vibration_signal = generate_vibration_data()

    if args.generate_training_data:
        # For training, we generate data without the anomaly
        print("Generating training data...")
        training_signal = generate_vibration_data(include_anomaly=False)
        with open('../data/training_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['sample_index', 'value'])
            for i, val in enumerate(training_signal):
                writer.writerow([i, val])
        print("Training data saved to '../data/training_data.csv'")
    else:
        # Otherwise, stream the data with the anomaly in real-time
        print("Starting real-time data stream simulation...")
        print("Press Ctrl+C to stop.")
        try:
            for sample_index, value in stream_data(vibration_signal, delay=0.05):
                # In a real project, we would call the detector here.
                # For now, we just yield the data.
                pass
        except KeyboardInterrupt:
            print("\nStream stopped by user.")

if __name__ == "__main__":
    main()
