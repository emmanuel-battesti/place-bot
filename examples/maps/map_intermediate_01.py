import math
import random
from typing import Type, Union

from spg.playground import Playground

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.map_abstract import MapAbstract

from .walls_intermediate_map_1 import add_walls, add_boxes


class MyMapIntermediate01(MapAbstract):

    def __init__(self, robot_type: Type[RobotAbstract]):
        super().__init__(robot_type=robot_type)

        # PARAMETERS MAP
        self._size_area = (800, 500)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        angle = random.uniform(-math.pi, math.pi)
        self._robot_pos = ((295, 118), angle)
        self._robot = robot_type()
        self._playground.add(self._robot, self._robot_pos)
