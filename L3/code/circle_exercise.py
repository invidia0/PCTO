# !/usr/bin/env python3

from pyniryo import *
import math


local_mode = False  # Or True
tool_used = ToolID.GRIPPER_1
# Set robot address
robot_ip_address = '10.10.10.10'
robot_ip_address_local = "127.0.0.1"

robot_ip_address = robot_ip_address_local if local_mode else robot_ip_address


def mm_to_m(val):
    if isinstance(val, list):
        return [x / 1000 for x in val]
    else:
        return val / 1000


def grad_to_rad(grad):
    return grad * math.pi / 180


def offset(pose1, pose2):
    return [p1 + p2 for p1, p2 in zip(pose1, pose2)]


def circle(robot, radius=0.1, height=0, n_points=10, n_circles=1):
    ...

def process(robot):
    ...


if __name__ == '__main__':
    # Connect to robot
    robot = NiryoRobot(robot_ip_address)
    # Calibrate robot if robot needs calibration
    robot.calibrate_auto()
    # Equip tool
    robot.update_tool()
    # Launching main process
    process(robot)
    # Ending
    robot.move_to_home_pose()
    # Releasing connection
    robot.close_connection()
