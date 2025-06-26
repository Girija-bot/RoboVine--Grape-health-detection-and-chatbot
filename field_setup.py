import pybullet as p
import pybullet_data
import os

def setup_field():
    print("Initializing PyBullet...")

    # Set gravity
    p.setGravity(0, 0, -9.8)

    # Load plane using absolute path from pybullet_data
    plane_path = os.path.join(pybullet_data.getDataPath(), "plane.urdf")
    print(f"Loading plane from: {plane_path}")
    try:
        plane_id = p.loadURDF(plane_path)
        print("Ground plane created.")
    except Exception as e:
        print(f"Failed to load plane.urdf: {e}")
        return None, []

    # Set additional search path for custom models
    custom_model_path = "C:/Users/girij/Distributed systems/models"
    p.setAdditionalSearchPath(custom_model_path)

    spacing = 0.5
    section_offset = 5
    plant_height = 0.1

    matrix = [
        [("ulcer", 5), ("gray_mold", 3), ("black_mold", 1)],
        [("gray_mold", 8), ("powdery_mildew", 7), ("sour_rot", 6)],
        [("powdery_mildew", 7), ("black_mold", 3), ("downy_mildew", 4)],
        [("mosaic_virus", 5), ("gray_mold", 4), ("black_mold", 2)],
        [("sour_rot", 6), ("mosaic_virus", 5), ("powdery_mildew", 3)],
        [("downy_mildew", 3), ("sour_rot", 1), ("ulcer", 8)],
    ]

    disease_colors = {
        "ulcer": [1, 0, 0, 1],
        "gray_mold": [0.5, 0.5, 0.5, 1],
        "black_mold": [0, 0, 0, 1],
        "powdery_mildew": [1, 1, 1, 1],
        "sour_rot": [1, 1, 0, 1],
        "mosaic_virus": [0, 1, 0, 1],
        "downy_mildew": [0, 0, 1, 1],
    }

    plants = []

    for row in range(2):
        for col in range(3):
            section_index = row * 3 + col
            diseases = matrix[section_index]
            base_x = col * section_offset
            base_y = row * section_offset

            px, py = 0, 0
            for disease, count in diseases:
                for _ in range(count):
                    pos = [base_x + px * spacing, base_y + py * spacing, plant_height]
                    visual = p.createVisualShape(
                        shapeType=p.GEOM_BOX,
                        halfExtents=[0.1, 0.1, 0.1],
                        rgbaColor=disease_colors[disease]
                    )
                    body = p.createMultiBody(baseVisualShapeIndex=visual, basePosition=pos)
                    plants.append({"id": body, "label": disease, "position": pos})
                    print(f"Planted {disease} at {pos}")
                    px += 1
                    if px > 4:
                        px = 0
                        py += 1

    try:
        robot = p.loadURDF("simple_robot.urdf", basePosition=[0, 0, 0.2])
        print("Robot loaded successfully.")
    except Exception as e:
        print(f"Failed to load robot: {e}")
        return None, plants

    return robot, plants
