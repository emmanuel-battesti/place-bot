"""
Simple random controller
The Robot will move forward and turn for a random angle when an obstacle is hit
"""
import math
import random

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.utils.utils import normalize_angle


class MyRobotRandom(RobotAbstract):
    def __init__(self,
                 **kwargs):
        super().__init__(should_display_lidar=False,
                         **kwargs)
        self.counterStraight = 0
        self.angleStopTurning = random.uniform(-math.pi, math.pi)
        self.distStopStraight = random.uniform(10, 50)
        self.isTurning = False

    def process_lidar_sensor(self):
        """
        Returns True if the robot hits an obstacle
        """
        if self.lidar().get_sensor_values() is None:
            return False

        touched = False
        min_distance = min(self.lidar().get_sensor_values())

        if min_distance < 30:
            touched = True

        return touched

    def control(self):
        """
        The Robot will move forward and turn for a random angle when an obstacle is hit
        """
        command_straight = {"forward": 1.0,
                            "rotation": 0.0}

        command_turn = {"forward": 0.0,
                        "rotation": 1.0}

        touched = self.process_lidar_sensor()

        self.counterStraight += 1

        if touched and not self.isTurning and self.counterStraight > self.distStopStraight:
            self.isTurning = True
            self.angleStopTurning = random.uniform(-math.pi, math.pi)

        measured_angle = 0
        if self.measured_compass_angle() is not None:
            measured_angle = self.measured_compass_angle()

        diff_angle = normalize_angle(self.angleStopTurning - measured_angle)
        if self.isTurning and abs(diff_angle) < 0.2:
            self.isTurning = False
            self.counterStraight = 0
            self.distStopStraight = random.uniform(10, 50)

        if self.isTurning:
            return command_turn
        else:
            return command_straight
