# !/usr/bin/env python3

from pyniryo import *
import math

local_mode = False  # Or True
tool_used = ToolID.GRIPPER_1
# Set robot address
robot_ip_address = '10.10.10.10'
robot_ip_address_local = "127.0.0.1"

example = {
    "joints": True,
    "pose": False,
    "linear": False,
    "advanced": False
}

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


def process(robot):
    # Attenzione alla posizione!! Se è non raggiungibile, il robot non si
    # muoverà.
    # [x, y, z, Roll, Pitch, Yaw] in metri e radianti, ricordati di convertirli!

    if example["joints"]:
        """ Joints Movement """
        joint_pose = [-0.5, -0.6, 0.0, 0.3, 0.0, 0.0]
        # Moving Joints with function & 6 floats
        robot.move_joints(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        # Moving Joints with function & a list of floats
        robot.move_joints(joint_pose)
        # Getting Joints with function
        joints_read = robot.get_joints()

    elif example["pose"]:
        """ Pose Movement """
        pose_target = [mm_to_m(200), 
                        0.0, 
                        mm_to_m(200), 
                        0.0, 
                        0.0, 
                        grad_to_rad(90)]
        robot.move_pose(pose_target)

    elif example["linear"]:
        """ Move linear """
        # Effettuerà un movimento lineare senza cambiare l'orientamento del gripper
        current_pose = robot.get_pose().to_list()
        pos1 = ([mm_to_m(200),
                mm_to_m(100),
                current_pose[2],
                current_pose[3],
                grad_to_rad(90),
                current_pose[5]])

        pos2 = ([mm_to_m(200),
                mm_to_m(-100),
                current_pose[2],
                current_pose[3],
                grad_to_rad(90),
                current_pose[5]])

        robot.move_pose(pos1)
        robot.move_linear_pose(pos2)

    elif example["advanced"]:
        """ Advanced use """
        positions = {
            "A": [mm_to_m(100), 0.0, mm_to_m(90), 0.0, 0.0, 0.0],
            "B": [mm_to_m(50), mm_to_m(100), mm_to_m(20), 0.0, 0.0, 0.0]
        }

        # Moving Pose with function (.get_pose() returns a PoseObject!)
        current_pose = robot.get_pose().to_list()
        offset_pose = mm_to_m(positions["B"])
        new_pose = offset(current_pose, offset_pose)
        robot.move_pose(new_pose)



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
