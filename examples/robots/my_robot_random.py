"""
Simple random controller
The Robot will move forward and turn for a random angle when an obstacle is hit
"""
import math
import random
from enum import Enum

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.utils.utils import normalize_angle


class State(Enum):
    STRAIGHT = 1
    TURN = 2


class MyRobotRandom(RobotAbstract):
    def __init__(self):
        super().__init__()
        self.counter_straight = random.randint(50, 100)
        self.target_angle = random.uniform(-math.pi, math.pi)
        self.state = State.STRAIGHT
        self.pause_after_turn = 0

    def process_lidar_sensor(self):
        """Detects if an obstacle is closer than a threshold."""
        sensor_values = self.lidar().get_sensor_values()
        if sensor_values is None:
            return False
        return min(sensor_values) < 20

    def control(self):
        """
        The Robot will move forward and turn for a random angle when an obstacle is hit.
        """
        command_straight = {"forward": 1.0, "rotation": 0.0}
        command_turn_left = {"forward": 0.0, "rotation": 1.0}
        command_turn_right = {"forward": 0.0, "rotation": -1.0}

        touched = self.process_lidar_sensor()
        measured_angle = 0
        if self.true_angle() is not None:
            measured_angle = self.true_angle()

        diff_angle = normalize_angle(self.target_angle - measured_angle)

        if (self.state == State.STRAIGHT and
                ((self.pause_after_turn == 0 and touched) or
                 self.counter_straight == 0)):
            # If the robot is go straight and
            #    it has touched an obstacle
            # or it has moved enough distance, then it will turn.

            # Transition to TURN state
            print(f"STRAIGHT => TURN, touched = {touched}")
            self.state = State.TURN
            # We set the target angle to a random value between -pi and pi
            self.target_angle = random.uniform(-math.pi, math.pi)

        elif self.state == State.TURN and abs(diff_angle) < 0.2:
            # If the robot is turning and it has turned enough
            # then it will go straight

            # Transition to STRAIGHT state
            print(f"TURN => STRAIGHT, diff = {diff_angle:.2f}")
            self.state = State.STRAIGHT
            self.pause_after_turn = 15
            self.counter_straight = random.randint(50, 100)

        if self.state == State.TURN:
            print(f"Turning, diff = {diff_angle:.2f}")
            if diff_angle > 0:
                return command_turn_left
            else:
                return command_turn_right
        else:
            if self.counter_straight > 0:
                self.counter_straight -= 1
            if self.pause_after_turn > 0:
                self.pause_after_turn -= 1
            print(
                f"Straight, touched = {touched}, counter = {self.counter_straight}, counterTurns = {self.pause_after_turn}")
            return command_straight
