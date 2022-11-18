import math
import random
from typing import List, Type

from spg.playground import Playground
from spg.utils.definitions import CollisionTypes

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.entities.rescue_center import RescueCenter, wounded_rescue_center_collision
from spg_overlay.entities.wounded_person import WoundedPerson
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.map_abstract import MapAbstract
from spg_overlay.utils.misc_data import MiscData

from .walls_complete_map_2 import add_walls, add_boxes


class MyMapComplete02(MapAbstract):

    def __init__(self):
        super().__init__()
        self._time_step_limit = 1200
        self._real_time_limit = 240  # In seconds

        # PARAMETERS MAP
        self._size_area = (1113, 750)

        self._rescue_center = RescueCenter(size=(210, 90))
        self._rescue_center_pos = ((440, 315), 0)

        self._wounded_persons_pos = [(-481, 175), (-511, -185), (-261, -175),
                                     (-81, 305), (-61, -175), (189, 315)]
        self._number_wounded_persons = len(self._wounded_persons_pos)
        self._wounded_persons: List[WoundedPerson] = []

        # POSITIONS OF THE ROBOTS
        self._number_robots = 10
        # They are positioned in a square whose side size depends on the total number of robots.
        start_area_robots = (439.0, 195)
        nb_per_side = math.ceil(math.sqrt(float(self._number_robots)))
        dist_inter_robot = 30.0
        # print("nb_per_side", nb_per_side)
        # print("dist_inter_robot", dist_inter_robot)
        sx = start_area_robots[0] - (nb_per_side - 1) * 0.5 * dist_inter_robot
        sy = start_area_robots[1] - (nb_per_side - 1) * 0.5 * dist_inter_robot
        # print("sx", sx, "sy", sy)

        self._robots_pos = []
        for i in range(self._number_robots):
            x = sx + (float(i) % nb_per_side) * dist_inter_robot
            y = sy + math.floor(float(i) / nb_per_side) * dist_inter_robot
            angle = random.uniform(-math.pi, math.pi)
            self._robots_pos.append(((x, y), angle))

        self._robots: List[RobotAbstract] = []

    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        playground = ClosedPlayground(size=self._size_area)

        # RESCUE CENTER
        playground.add_interaction(CollisionTypes.GEM,
                                   CollisionTypes.ACTIVABLE_BY_GEM,
                                   wounded_rescue_center_collision)

        playground.add(self._rescue_center, self._rescue_center_pos)

        add_walls(playground)
        add_boxes(playground)

        self._explored_map.initialize_walls(playground)

        # POSITIONS OF THE WOUNDED PERSONS
        for i in range(self._number_wounded_persons):
            wounded_person = WoundedPerson(rescue_center=self._rescue_center)
            self._wounded_persons.append(wounded_person)
            pos = (self._wounded_persons_pos[i], 0)
            playground.add(wounded_person, pos)

        # POSITIONS OF THE ROBOTS
        misc_data = MiscData(size_area=self._size_area,
                             number_robots=self._number_robots)
        for i in range(self._number_robots):
            robot = robot_type(identifier=i, misc_data=misc_data)
            self._robots.append(robot)
            playground.add(robot, self._robots_pos[i])

        return playground
