import math
import random
from typing import List, Type, Union

from spg.playground import Playground
from spg.utils.definitions import CollisionTypes

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.map_abstract import MapAbstract

from .walls_complete_map_1 import add_walls, add_boxes


class MyMapComplete01(MapAbstract):

    def __init__(self):
        super().__init__()
        self._time_step_limit = 1200
        self._real_time_limit = 240  # In seconds

        # PARAMETERS MAP
        self._size_area = (1110, 750)

        # POSITION OF THE ROBOT
        angle = random.uniform(-math.pi, math.pi)
        self._robot_pos = ((-375, -300), angle)
        self._robot: Union[RobotAbstract, Type[None]] = None

    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        playground = ClosedPlayground(size=self._size_area)

        add_walls(playground)
        add_boxes(playground)

        # POSITION OF THE ROBOT
        self._robot = robot_type()
        playground.add(self._robot, self._robot_pos)

        return playground
