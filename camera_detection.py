import cv2
import numpy as np

# Simulate a camera view
def simulate_camera(robot_position, plant_positions):
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    for plant_pos in plant_positions:
        plant_x, plant_y = int(plant_pos[0] * 50 + 250), int(plant_pos[1] * 50 + 250)
        cv2.circle(img, (plant_x, plant_y), 10, (0, 255, 0), -1)  # Green dots for plants
    return img

# Detect green areas as plants
def detect_plants_with_camera(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 100, 50])  # Adjust for a more specific green
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    detected_positions = cv2.findNonZero(mask)
    return detected_positions
