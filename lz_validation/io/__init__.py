"""Module for any IO operations."""
import json
import os


def save_metrics_to_file(metrics, metrics_file):
    if os.path.exists(metrics_file):
        with open(metrics_file) as f:
            metrics.update(json.load(f))
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f)
