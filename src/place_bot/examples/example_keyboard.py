"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import Type

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.gui_sr import GuiSR
from spg_overlay.gui_map.map_abstract import MapAbstract


class MyRobotKeyboard(RobotAbstract):
    def control(self):
        command = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyMapKeyboard(MapAbstract):

    def __init__(self, robot_type: Type[RobotAbstract]):
        super().__init__(robot_type=robot_type)

        # PARAMETERS MAP
        self._size_area = (600, 600)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        self._robot_pos = ((0, 0), 0)
        self._robot = robot_type()
        self._playground.add(self._robot, self._robot_pos)


def print_keyboard_man():
    print("How to use the keyboard to direct the robot?")
    print("\t- up / down key : forward and backward")
    print("\t- left / right key : turn left / right")
    print("\t- l key : display (or not) the lidar sensor")
    print("\t- q key : exit the program")
    print("\t- r key : reset")


if __name__ == '__main__':
    print_keyboard_man()
    my_map = MyMapKeyboard(robot_type=MyRobotKeyboard)

    # draw_lidar : enable the visualization of the lidar rays
    gui = GuiSR(the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                )
    gui.run()

