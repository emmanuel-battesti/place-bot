import math
import random

from place_bot.simulation.old_entities.robot_abstract import RobotAbstract
from place_bot.simulation.old_simu_world import ClosedPlayground
from place_bot.simulation.old_simu_world import WorldAbstract

from .walls_complete_world_2 import add_walls, add_boxes


class MyWorldComplete02(WorldAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (1113, 750)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        angle = random.uniform(-math.pi, math.pi)
        self._robot_pos = ((439.0, 195), angle)
        self._playground.add(robot, self._robot_pos)
