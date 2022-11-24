import math
import random
from typing import Type

from spg.playground import Playground

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.map_abstract import MapAbstract


class MyMapRandom(MapAbstract):

    def __init__(self):
        super().__init__()

        self._size_area = (1500, 700)

        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        x = random.uniform(-self._size_area[0]/2, self._size_area[0]/2)
        y = random.uniform(-self._size_area[1]/2, self._size_area[1]/2)
        angle = random.uniform(-math.pi, math.pi)
        self._playground.add(self._robot, ((x, y), angle))
