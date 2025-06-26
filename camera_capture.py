import pybullet as p
import numpy as np
import cv2

def capture_camera_image(robot):
    """
    Capture an image from the robot's camera.
    :param robot: The robot object
    :return: Captured RGB image
    """
    position, _ = p.getBasePositionAndOrientation(robot)

    # Camera parameters
    view_matrix = p.computeViewMatrixFromYawPitchRoll(
        cameraTargetPosition=position, distance=1.0, yaw=0, pitch=-30, roll=0, upAxisIndex=2
    )
    projection_matrix = p.computeProjectionMatrixFOV(
        fov=60, aspect=1.0, nearVal=0.1, farVal=10.0
    )

    # Capture image
    _, _, rgb_image, _, _ = p.getCameraImage(
        width=512, height=512, viewMatrix=view_matrix, projectionMatrix=projection_matrix
    )
    rgb_image = np.reshape(rgb_image, (512, 512, 4))[:, :, :3]
    return rgb_image

def save_image(image, filename):
    """
    Save an image to disk.
    :param image: RGB image
    :param filename: File name for saving the image
    """
    cv2.imwrite(filename, image)
    print(f"Image saved: {filename}")
