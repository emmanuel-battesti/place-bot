"""
This program can be launched directly.
"""

import math
import os
import random
import sys

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worlds.world_intermediate_01 import MyWorldIntermediate01
from place_bot.simulation.entities.robot_abstract import RobotAbstract
from place_bot.simulation.simu_world.simulator import Simulator
from place_bot.simulation.utils.utils import normalize_angle


class MyRobotRandom(RobotAbstract):
    def __init__(self):
        super().__init__()
        self.counterStraight = 0
        self.angleStopTurning = random.uniform(-math.pi, math.pi)
        self.counterStopStraight = random.uniform(10, 30)
        self.isTurningLeft = False
        self.isTurningRight = False

    def control(self) -> CommandsDict:
        """
        The Robot will move forward and turn for a random angle when an obstacle is hit
        """
        command_straight = {"forward": 1.0,
                            "rotation": 0.0}
        command_turn_left = {"forward": 0.0,
                             "rotation": 1.0}
        command_turn_right = {"forward": 0.0,
                              "rotation": -1.0}

        self.counterStraight += 1

        if not self._is_turning() and self.counterStraight > self.counterStopStraight:
            self.angleStopTurning = random.uniform(-math.pi, math.pi)
            diff_angle = normalize_angle(self.angleStopTurning - self.angle)
            if diff_angle > 0:
                self.isTurningLeft = True
            else:
                self.isTurningRight = True

        diff_angle = normalize_angle(self.angleStopTurning - self.angle)
        if self._is_turning() and abs(diff_angle) < 0.2:
            self.isTurningLeft = False
            self.isTurningRight = False
            self.counterStraight = 0
            self.counterStopStraight = random.uniform(10, 30)

        # print("\nself.isTurning : {}, abs(diff_angle) = {}".format(self.isTurning, abs(diff_angle)))
        # print("self.angleStopTurning = {}, self.angle = {}, diff_angle = {}".format(self.angleStopTurning, self.angle, diff_angle))
        if self.isTurningLeft:
            return command_turn_left
        elif self.isTurningRight:
            return command_turn_right
        else:
            return command_straight

    def _is_turning(self):
        return self.isTurningLeft or self.isTurningRight


def main():
    my_robot = MyRobotRandom()
    my_world = MyWorldIntermediate01(robot=my_robot)

    simulator = Simulator(the_world=my_world,
                          use_keyboard=False,
                          use_mouse_measure=True,
                          enable_visu_noises=False,
                          )
    simulator.run()

if __name__ == '__main__':
    main()