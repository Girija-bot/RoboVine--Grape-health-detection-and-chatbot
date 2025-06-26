from PIL import Image
import numpy as np
from collections import Counter

# Disease color mapping
disease_colors = {
    "ulcer": ([1, 0, 0, 1], "Red"),
    "gray_mold": ([0.5, 0.5, 0.5, 1], "Gray"),
    "black_mold": ([0, 0, 0, 1], "Black"),
    "powdery_mildew": ([1, 1, 1, 1], "White"),
    "sour_rot": ([1, 1, 0, 1], "Yellow"),
    "mosaic_virus": ([0, 1, 0, 1], "Green"),
    "downy_mildew": ([0, 0, 1, 1], "Blue"),
}

def get_dominant_color(image_path):
    img = Image.open(image_path).convert('RGBA')
    img = img.resize((50, 50))  # Resize to speed up
    pixels = np.array(img).reshape(-1, 4)  # Flatten pixels
    counts = Counter(map(tuple, pixels))
    dominant_pixel = counts.most_common(1)[0][0]
    # Normalize to 0-1
    return [x / 255.0 for x in dominant_pixel]

def color_distance(c1, c2):
    return np.linalg.norm(np.array(c1[:3]) - np.array(c2[:3]))  # Ignore alpha

# Path to image
image_path = "C:/Users/girij/Distributed systems/captured_images/image_3935.png"
dominant_color = get_dominant_color(image_path)
print(f"Dominant color (normalized RGBA): {dominant_color}")

# Match with disease colors
min_dist = float('inf')
closest_disease = None

for disease, (ref_color, name) in disease_colors.items():
    dist = color_distance(dominant_color, ref_color)
    if dist < min_dist:
        min_dist = dist
        closest_disease = (disease, name, ref_color, dist)

# Threshold to ignore wrong guesses
if closest_disease and closest_disease[3] < 0.3:
    disease, name, color, dist = closest_disease
    print(f"Disease Detected: {disease.upper()} ({name}) | Distance: {dist:.2f}")
else:
    print("No disease detected confidently. Closest color doesn't match well.")
