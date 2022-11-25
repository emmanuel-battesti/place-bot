import math
import random
from typing import Type

from spg.playground import Playground

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.map_abstract import MapAbstract

from .walls_complete_map_1 import add_walls, add_boxes


class MyMapComplete01(MapAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS MAP
        self._size_area = (1110, 750)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        angle = random.uniform(-math.pi, math.pi)
        self._robot_pos = ((-375, -300), angle)
        self._playground.add(robot, self._robot_pos)
