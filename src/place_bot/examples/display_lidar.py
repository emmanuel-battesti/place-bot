"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import Type

from spg.playground import Playground

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maps.walls_complete_map_2 import add_walls, add_boxes
from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.gui_sr import GuiSR
from spg_overlay.gui_map.map_abstract import MapAbstract


class MyRobotLidar(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def control(self):
        """
        We only send a command to do nothing
        """
        command = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyMapLidar(MapAbstract):

    def __init__(self):
        super().__init__()

        # PARAMETERS MAP
        self._size_area = (1113, 750)

        # POSITION OF THE ROBOT
        self._robot_pos = ((-50, 0), 0)

    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        playground = ClosedPlayground(size=self._size_area)

        add_walls(playground)
        add_boxes(playground)

        # POSITION OF THE ROBOT
        self._robot = robot_type(should_display_lidar=True)
        playground.add(self._robot, self._robot_pos)

        return playground


def main():
    my_map = MyMapLidar()
    playground = my_map.construct_playground(robot_type=MyRobotLidar)

    # draw_lidar : enable the visualization of the lidar rays
    # enable_visu_noises : to enable the visualization. It will show also a demonstration of the integration
    # of odometer values, by drawing the estimated path in red.
    gui = GuiSR(playground=playground,
                the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                enable_visu_noises=True,
                )
    gui.run()


if __name__ == '__main__':
    main()
