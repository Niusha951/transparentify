"""
make_transparent.py

This script processes an input image by:
1. Making near-white background pixels fully transparent.
2. Converting near-black lines to pure white and fully opaque.

Usage:
    Update the 'image_path' variable with the input image filename.
    Run the script to generate a new image with transparency applied.
"""

import cv2
import numpy as np

# Input and output image paths
image_path = "example.png"
output_path = "example_transparent.png"

# Load the image (in BGR format)
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found at path: {image_path}")

# Convert the image to BGRA (adds an alpha channel)
image_bgra = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

# Convert image to RGB format for color thresholding (easier for human interpretation)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ----- Step 1: Make near-white background transparent -----
# Define RGB thresholds for what is considered "near-white"
white_lower = np.array([240, 240, 240], dtype=np.uint8)
white_upper = np.array([255, 255, 255], dtype=np.uint8)

# Create a mask for near-white pixels
white_mask = cv2.inRange(image_rgb, white_lower, white_upper)

# Set alpha to 0 (fully transparent) for pixels matching the white mask
image_bgra[white_mask > 0, 3] = 0

# ----- Step 2: Convert near-black lines to solid white and fully opaque -----
# Define RGB thresholds for what is considered "near-black"
black_lower = np.array([0, 0, 0], dtype=np.uint8)
black_upper = np.array([30, 30, 30], dtype=np.uint8)

# Create a mask for near-black pixels
black_mask = cv2.inRange(image_rgb, black_lower, black_upper)

# Set BGR to white and alpha to 255 (fully opaque) for detected black lines
image_bgra[black_mask > 0, :3] = [255, 255, 255]  # Set color to white
image_bgra[black_mask > 0, 3] = 255               # Set alpha to fully opaque

# Save the resulting image (in BGRA format)
cv2.imwrite(output_path, image_bgra)
print(f"Saved modified image to: {output_path}")

