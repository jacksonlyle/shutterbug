#!/usr/bin/env python3
"""
spectral_to_csv.py

Extracts a 1D spectrum by averaging the middle 20 rows of a grayscale image
and writes out a CSV with columns: pixel,intensity
"""

import sys
import cv2
import numpy as np
import pandas as pd

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python spectral_to_csv.py <input_image> [output_csv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else "spectrum_data.csv"

    # 1. Load the image in grayscale
    img = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: could not load image '{input_file}'")
        sys.exit(1)

    height, width = img.shape
    print(f"Loaded image '{input_file}' (width={width}, height={height})")

    # 2. Define the middle 20 rows
    center_row = height // 2
    half_window = 20 // 2
    y_start = max(center_row - half_window, 0)
    y_end   = min(center_row + half_window, height)
    print(f"Averaging rows {y_start} through {y_end - 1} (total {y_end - y_start} rows)")

    # 3. Compute the mean intensity for each column
    #    Result is a 1D array of length=width
    intensity_profile = img[y_start:y_end, :].mean(axis=0)

    # 4. Build a DataFrame and export to CSV
    df = pd.DataFrame({
        "pixel":     np.arange(width),
        "intensity": intensity_profile
    })
    df.to_csv(output_file, index=False)
    print(f"Wrote {len(df)} rows to '{output_file}'")

if __name__ == "__main__":
    main()