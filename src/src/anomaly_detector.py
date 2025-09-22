#!/usr/bin/env python3
"""
The core anomaly detection logic. Trains a baseline model and checks new data against it.
"""

import numpy as np
import json
import argparse
import csv
from pathlib import Path

class AnomalyDetector:
    def __init__(self, window_size=10, threshold=2.5):
        self.window_size = window_size
        self.threshold = threshold # k value, higher = less sensitive
        self.baseline_mean = None
        self.baseline_std = None

    def train(self, data):
        """Establishes the baseline 'normal' parameters from training data."""
        print("Training anomaly detector...")
        self.baseline_mean = np.mean(data)
        self.baseline_std = np.std(data)
        print(f"Baseline established: Mean = {self.baseline_mean:.4f}, Std = {self.baseline_std:.4f}")
        return self

    def check_anomaly(self, data_window):
        """Checks a window of data for anomalies against the trained baseline."""
        if self.baseline_mean is None:
            raise ValueError("Detector must be trained before use.")

        current_mean = np.mean(data_window)
        current_std = np.std(data_window)

        # Check if current stats deviate from baseline beyond the threshold
        mean_diff = abs(current_mean - self.baseline_mean)
        std_diff = abs(current_std - self.baseline_std)

        if mean_diff > self.threshold * self.baseline_std or std_diff > self.threshold * self.baseline_std:
            return True, current_mean, current_std
        else:
            return False, current_mean, current_std

def main():
    parser = argparse.ArgumentParser(description='Anomaly Detection Model')
    parser.add_argument('--train', action='store_true', help='Train the model on the training data')
    args = parser.parse_args()

    # Create necessary directories
    Path('../models').mkdir(exist_ok=True)
    Path('../data').mkdir(exist_ok=True)

    if args.train:
        # Load training data
        try:
            data = np.genfromtxt('../data/training_data.csv', delimiter=',', skip_header=1, usecols=1)
        except FileNotFoundError:
            print("Error: Training data not found. Run 'python data_simulator.py --generate_training_data' first.")
            return

        # Train the model
        detector = AnomalyDetector()
        detector.train(data)

        # Save the model parameters (like you would save a model on Arduino)
        model_params = {
            "baseline_mean": float(detector.baseline_mean),
            "baseline_std": float(detector.baseline_std),
            "threshold": detector.threshold
        }
        with open('../models/baseline_params.json', 'w') as f:
            json.dump(model_params, f, indent=4)
        print("Model parameters saved to '../models/baseline_params.json'")

    # For the purposes of this demo, we'll also run a test.
    if not args.train:
        print("Please use the --train flag to train the model.")

if __name__ == "__main__":
    main()
