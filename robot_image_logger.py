import pybullet as p
import pybullet_data
import time
import os
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import keyboard
import csv

# Constants
CSV_LOG_PATH = "simulation_log.csv"
output_dir = "captured_images"
os.makedirs(output_dir, exist_ok=True)

# Connect to PyBullet
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Load plane
planeId = p.loadURDF("plane.urdf")
print("Ground plane created.")

# Load robot
robot_start_pos = [0, 0, 0.1]
robot_urdf_path = r"C:\Users\girij\Distributed systems\models\simple_robot.urdf"
robot = p.loadURDF(robot_urdf_path, robot_start_pos)
print("Robot loaded successfully.")

# Define 2x3 matrix with 48 plant IDs
grid_matrix = {
    (0, 0): ['A10', 'B01', 'B05', 'B12', 'B14', 'C04', 'C12', 'C16'],
    (0, 1): ['C17', 'D07', 'D13', 'D15', 'B02', 'B06', 'B07', 'B09'],
    (0, 2): ['B15', 'C01', 'C09', 'C10', 'D05', 'D09', 'D11', 'D18'],
    (1, 0): ['A01', 'A04', 'A08', 'A11', 'A13', 'B08', 'B10', 'C11'],
    (1, 1): ['C14', 'C15', 'D04', 'D14', 'A09', 'A14', 'A18', 'B04'],
    (1, 2): ['B11', 'B17', 'C03', 'C06', 'C07', 'D12', 'D16', 'D17']
}

# Get plant IDs for a grid cell
def get_plant_ids_for_position(grid_x, grid_y):
    return grid_matrix.get((grid_x, grid_y), [])

# Setup field with visual placeholder plants
def setup_field():
    plant_urdf_path = os.path.join(pybullet_data.getDataPath(), "cube_small.urdf")
    plant_spacing = 0.25
    cell_spacing = 1.5
    base_z = 0.0
    plants = []

    for (grid_x, grid_y), plant_ids in grid_matrix.items():
        base_x = grid_x * cell_spacing
        base_y = grid_y * cell_spacing

        for idx, label in enumerate(plant_ids):
            px = base_x + (idx % 4) * plant_spacing
            py = base_y + (idx // 4) * plant_spacing
            plant_id = p.loadURDF(plant_urdf_path, [px, py, base_z])
            plants.append((plant_id, label))
            print(f"Planted {label} at ({px:.2f}, {py:.2f})")

    return robot, plants

# Move robot in direction
def move_robot(robot_id, position, direction):
    step_size = 0.2
    x, y, z = position
    if direction == 'forward':
        x += step_size
    elif direction == 'backward':
        x -= step_size
    elif direction == 'left':
        y -= step_size
    elif direction == 'right':
        y += step_size
    new_pos = [x, y, z]
    p.resetBasePositionAndOrientation(robot_id, new_pos, [0, 0, 0, 1])
    return new_pos

# Capture image and log metadata
def capture_and_save_image(robot_id, count, position_for_filename=None, plant_ids=None):
    try:
        pos, orn = p.getBasePositionAndOrientation(robot_id)
        view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=pos,
            distance=1.5,
            yaw=50,
            pitch=-20,
            roll=0,
            upAxisIndex=2
        )
        proj_matrix = p.computeProjectionMatrixFOV(
            fov=60, aspect=1.0, nearVal=0.1, farVal=100
        )
        img_arr = p.getCameraImage(224, 224, view_matrix, proj_matrix)
        rgb_img = np.reshape(img_arr[2], (224, 224, 4))[:, :, :3]

        if position_for_filename:
            filename = f"capture_{count}_x{position_for_filename[0]}_y{position_for_filename[1]}.png"
        else:
            filename = f"capture_{count}.png"

        image_filename = os.path.join(output_dir, filename)
        cv2.imwrite(image_filename, rgb_img)
        print(f"Saved {image_filename}")

        plant_str = ', '.join(map(str, plant_ids)) if plant_ids else ""

        data_row = {
            "image_name": filename,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "plant_ids": plant_str,
            "Initial_Weight": 1,
            "Mean_Biomass_Gain": round(np.random.uniform(1.7, 2.2), 6),
            "Mean_Transpiration_Rate": round(np.random.uniform(1.7, 2.2), 6),
            "Mean_Daily_Transpiration": round(np.random.uniform(-2.2, -1.9), 6),
            "Theta_Crit": np.nan,
            "Stress_Degree": round(np.random.uniform(1.0, 1.2), 6),
            "Resilience_Rate": np.nan,
            "Stress_Label": np.random.choice([0, 1])
        }

        columns = [
            "image_name", "timestamp", "plant_ids",
            "Initial_Weight", "Mean_Biomass_Gain", "Mean_Transpiration_Rate",
            "Mean_Daily_Transpiration", "Theta_Crit", "Stress_Degree",
            "Resilience_Rate", "Stress_Label"
        ]

        df = pd.DataFrame([data_row], columns=columns)
        write_header = not os.path.exists(CSV_LOG_PATH)

        df.to_csv(
            CSV_LOG_PATH,
            mode='a',
            header=write_header,
            index=False,
            na_rep='NA',
            quoting=csv.QUOTE_NONNUMERIC
        )

    except Exception as e:
        print(f"⚠️ Error capturing or logging image {count}: {e}")

# Convert position to grid cell
def get_grid_position(position):
    return int(round(position[0])), int(round(position[1]))

# Setup field
print("Setting up the field...")
robot, plants = setup_field()
if not robot:
    print("❌ Robot initialization failed.")
    time.sleep(5)
    p.disconnect()
    exit()

robot_position = [0, 0, 0.2]
step = 0
visited_cells = set()

# Main loop
try:
    print("Use 'f', 'b', 'l', 'r' to move the robot (Ctrl+C to quit).")
    while True:
        if keyboard.is_pressed('f'):
            robot_position = move_robot(robot, robot_position, 'forward')
        elif keyboard.is_pressed('b'):
            robot_position = move_robot(robot, robot_position, 'backward')
        elif keyboard.is_pressed('l'):
            robot_position = move_robot(robot, robot_position, 'left')
        elif keyboard.is_pressed('r'):
            robot_position = move_robot(robot, robot_position, 'right')

        grid_x, grid_y = get_grid_position(robot_position)

        if 0 <= grid_x <= 1 and 0 <= grid_y <= 2:
            if (grid_x, grid_y) not in visited_cells:
                print(f"📍 Visiting new cell: ({grid_x}, {grid_y})")
                plant_ids = get_plant_ids_for_position(grid_x, grid_y)
                capture_and_save_image(robot, step, [grid_x, grid_y, robot_position[2]], plant_ids)
                visited_cells.add((grid_x, grid_y))

        p.stepSimulation()
        time.sleep(0.1)
        step += 1

except KeyboardInterrupt:
    print("\n🛑 Simulation interrupted by user.")
finally:
    p.disconnect()
    print("✅ Simulation ended.")
