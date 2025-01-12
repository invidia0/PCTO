# !/usr/bin/env python3

from pyniryo import *
import math

def mm_to_m(val):
    if isinstance(val, list):
        return [x / 1000 for x in val]
    else:
        return val / 1000


def grad_to_rad(grad):
    return grad * math.pi / 180


def offset(pose1, pose2):
    return [p1 + p2 for p1, p2 in zip(pose1, pose2)]


local_mode = False  # Or True
tool_used = ToolID.GRIPPER_1
# Set robot address
robot_ip_address = '10.10.10.10'
robot_ip_address_local = "127.0.0.1"

robot_ip_address = robot_ip_address_local if local_mode else robot_ip_address

pick_pose = PoseObject(
    x=mm_to_m(180),
    y=mm_to_m(100),
    z=mm_to_m(40),
    roll=0.0,
    pitch=grad_to_rad(90),
    yaw=0.0
)

place_pose = PoseObject(
    x=mm_to_m(180),
    y=mm_to_m(-100),
    z=mm_to_m(40),
    roll=0.0,
    pitch=grad_to_rad(90),
    yaw=0.0
)


def pick_n_place_version_1(robot):
    height_offset = mm_to_m(50)

    pick_pose_high = pick_pose.copy_with_offsets(z_offset=height_offset)
    place_pose_high = place_pose.copy_with_offsets(z_offset=height_offset)

    # Going Over Object
    robot.move_pose(pick_pose_high)
    # Opening Gripper
    robot.release_with_tool()
    # Going to picking place and closing gripper
    robot.move_pose(pick_pose)
    robot.grasp_with_tool()
    # Raising
    robot.move_pose(pick_pose_high)

    # Going Over Place pose
    robot.move_pose(place_pose_high)
    # Going to Place pose
    robot.move_pose(place_pose)
    # Opening Gripper
    robot.release_with_tool()
    # Raising
    robot.move_pose(place_pose_high)


"""
Con la seguente funzione non avete controllo su tutte le fasi! Usare con cautela.
"""
# def pick_n_place_version_2(robot):
#     # Pick
#     robot.pick_from_pose(pick_pose)
#     # Place
#     robot.place_from_pose(place_pose)


if __name__ == '__main__':
    # Connect to robot
    robot = NiryoRobot(robot_ip_address)
    # Calibrate robot if robot needs calibration
    robot.calibrate_auto()
    # Equip tool
    robot.update_tool()
    # Launching main process
    pick_n_place_version_1(robot)
    # Ending
    robot.move_to_home_pose()
    # Releasing connection
    robot.close_connection()
