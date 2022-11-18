"""
This program can be launched directly.
To move the robot, you have to click on the map, then use the arrows on the keyboard
"""

import os
import sys
from typing import List, Type

from spg.utils.definitions import CollisionTypes

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spg_overlay.entities.robot_abstract import RobotAbstract
from spg_overlay.gui_map.closed_playground import ClosedPlayground
from spg_overlay.gui_map.gui_sr import GuiSR
from spg_overlay.gui_map.map_abstract import MapAbstract


class MyRobotKeyboard(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def control(self):
        command = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyMapKeyboard(MapAbstract):

    def __init__(self):
        super().__init__()

        # PARAMETERS MAP
        self._size_area = (600, 600)

        # POSITION OF THE ROBOT
        self._robot_pos = ((0, 0), 0)

    def construct_playground(self, robot_type: Type[RobotAbstract]):
        playground = ClosedPlayground(size=self._size_area)

        # POSITION OF THE ROBOT
        self._robot = robot_type()
        playground.add(self._robot, self._robot_pos)

        return playground


def print_keyboard_man():
    print("How to use the keyboard to direct the robot?")
    print("\t- up / down key : forward and backward")
    print("\t- left / right key : turn left / right")
    print("\t- l key : display (or not) the lidar sensor")
    print("\t- q key : exit the program")
    print("\t- r key : reset")


def main():
    print_keyboard_man()
    my_map = MyMapKeyboard()

    playground = my_map.construct_playground(robot_type=MyRobotKeyboard)

    # draw_lidar : enable the visualization of the lidar rays
    gui = GuiSR(playground=playground,
                the_map=my_map,
                draw_lidar=True,
                use_keyboard=True,
                )
    gui.run()


if __name__ == '__main__':
    main()
