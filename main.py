import pybullet as p
import time
import keyboard
import numpy as np
import cv2
import os
from field_setup import setup_field
from robot_movement import move_robot

# Connect to PyBullet GUI
p.connect(p.GUI)

# Directory to save captured images
CAPTURED_IMAGES_DIR = "captured_images"
if not os.path.exists(CAPTURED_IMAGES_DIR):
    os.makedirs(CAPTURED_IMAGES_DIR)


def capture_and_save_image(robot, step, position):
    try:
        camera_distance = 1.0
        camera_yaw = 0
        camera_pitch = -30

        view_matrix = p.computeViewMatrixFromYawPitchRoll(
            cameraTargetPosition=position,
            distance=camera_distance,
            yaw=camera_yaw,
            pitch=camera_pitch,
            roll=0,
            upAxisIndex=2
        )
        projection_matrix = p.computeProjectionMatrixFOV(
            fov=60, aspect=1.0, nearVal=0.1, farVal=10.0
        )

        width, height, rgb_img, _, _ = p.getCameraImage(
            width=224, height=224, viewMatrix=view_matrix, projectionMatrix=projection_matrix
        )

        rgb_img = np.reshape(rgb_img, (height, width, 4))
        rgb_img = rgb_img[:, :, :3]

        image_filename = f"image_{step}.png"
        image_path = os.path.join(CAPTURED_IMAGES_DIR, image_filename)
        cv2.imwrite(image_path, rgb_img)
        print(f"Image captured and saved: {image_path}")

    except Exception as e:
        print(f"Error capturing and saving image: {e}")

# Initialize simulation
print("Setting up the field...")
robot, plants = setup_field()

if not robot:
    print("Robot initialization failed.")
    time.sleep(5)
    p.disconnect()
    exit()

robot_position = [0, 0, 0.2]
step = 0

def get_grid_position(position):
    return int(round(position[0])), int(round(position[1]))

visited_cells = set()

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
        if (grid_x, grid_y) not in visited_cells:
            print(f"Visiting new cell: ({grid_x}, {grid_y})")
            capture_and_save_image(robot, step, [grid_x, grid_y, robot_position[2]])
            visited_cells.add((grid_x, grid_y))

        p.stepSimulation()
        time.sleep(0.01)
        step += 1

except KeyboardInterrupt:
    print("\nSimulation interrupted.")

finally:
    p.disconnect()
    print("Simulation ended.")
