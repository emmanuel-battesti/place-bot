import math
import random
from typing import Type

from spg.playground import Playground

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.simu_world.closed_playground import ClosedPlayground
from place_bot.simu_world.world_abstract import WorldAbstract


class MyWorldRandom(WorldAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (1500, 700)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        x = random.uniform(-self._size_area[0]/2, self._size_area[0]/2)
        y = random.uniform(-self._size_area[1]/2, self._size_area[1]/2)
        angle = random.uniform(-math.pi, math.pi)
	self._robot_pos = ((x, y), angle)
        self._playground.add(robot, self._robot_pos)
