import pybullet as p

def move_robot(robot, position, direction, step_size=0.05):
    """
    Move the robot in a specified direction.

    :param robot: The robot object
    :param position: Current position of the robot
    :param direction: String ('forward', 'backward', 'left', 'right')
    :param step_size: Step size for movement in meters
    :return: Updated position
    """
    if direction == 'forward':
        new_position = [position[0] + step_size, position[1], position[2]]
    elif direction == 'backward':
        new_position = [position[0] - step_size, position[1], position[2]]
    elif direction == 'left':
        new_position = [position[0], position[1] + step_size, position[2]]
    elif direction == 'right':
        new_position = [position[0], position[1] - step_size, position[2]]
    else:
        new_position = position  # No movement if direction is invalid

    # Update robot's position in the simulation
    p.resetBasePositionAndOrientation(robot, new_position, [0, 0, 0, 1])
    return new_position
