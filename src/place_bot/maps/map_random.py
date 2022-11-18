import math
import random
from typing import List, Type

from spg.playground import Playground

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.entities.wounded_person import WoundedPerson
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.map_abstract import MapAbstract


class MyMapRandom(MapAbstract):

    def __init__(self):
        super().__init__()
        self._number_robots = 10
        self._time_step_limit = 480
        self._real_time_limit = 22  # In seconds
        self._size_area = (1500, 700)
        self._wounded_persons: List[WoundedPerson] = []

    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        playground = ClosedPlayground(size=self._size_area)

        # POSITIONS OF THE ROBOTS
        for i in range(self._number_robots):
            x = random.uniform(-self._size_area[0]/2, self._size_area[0]/2)
            y = random.uniform(-self._size_area[1]/2, self._size_area[1]/2)
            angle = random.uniform(-math.pi, math.pi)
            playground.add(self._robots[i], ((x, y), angle))

        return playground
