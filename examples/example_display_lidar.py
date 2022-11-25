"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import Type

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from maps.walls_complete_map_2 import add_walls, add_boxes
from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.gui_sr import GuiSR
from place_bot.gui_map.map_abstract import MapAbstract


class MyRobotLidar(RobotAbstract):
    def control(self):
        """
        We only send a command to do nothing
        """
        command = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyMapLidar(MapAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS MAP
        self._size_area = (1113, 750)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        self._robot_pos = ((-50, 0), 0)
        self._playground.add(robot, self._robot_pos)


if __name__ == '__main__':
    my_robot = MyRobotLidar(should_display_lidar=True)
    my_map = MyMapLidar(robot=my_robot)

    # draw_lidar : enable the visualization of the lidar rays
    # enable_visu_noises : to enable the visualization. It will show also a demonstration of the integration
    # of odometer values, by drawing the estimated path in red.
    gui = GuiSR(the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                enable_visu_noises=True,
                )
    gui.run()
