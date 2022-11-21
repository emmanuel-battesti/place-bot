import math
import random
from typing import Type, Union

from spg.playground import Playground

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.map_abstract import MapAbstract

from .walls_complete_map_1 import add_walls, add_boxes


class MyMapComplete01(MapAbstract):

    def __init__(self, robot_type: Type[RobotAbstract]):
        super().__init__(robot_type=robot_type)

        # PARAMETERS MAP
        self._size_area = (1110, 750)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        angle = random.uniform(-math.pi, math.pi)
        self._robot_pos = ((-375, -300), angle)
        self._robot = robot_type()
        self._playground.add(self._robot, self._robot_pos)

