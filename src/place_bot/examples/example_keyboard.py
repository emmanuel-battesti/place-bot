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
from spg_overlay.utils.misc_data import MiscData


class MyRobotKeyboard(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def define_message_for_all(self):
        """
        Here, we don't need communication...
        """
        pass

    def control(self):
        command = {"forward": 0.0,
                   "lateral": 0.0,
                   "rotation": 0.0,
                   "grasper": 0}
        return command


class MyMapKeyboard(MapAbstract):

    def __init__(self):
        super().__init__()

        # PARAMETERS MAP
        self._size_area = (600, 600)

        self._number_robots = 1
        self._robots_pos = [((0, 0), 0)]
        self._robots = []

    def construct_playground(self, robot_type: Type[RobotAbstract]):
        playground = ClosedPlayground(size=self._size_area)

        # POSITIONS OF THE ROBOTS
        misc_data = MiscData(size_area=self._size_area,
                             number_robots=self._number_robots)
        for i in range(self._number_robots):
            robot = robot_type(identifier=i, misc_data=misc_data)
            self._robots.append(robot)
            playground.add(robot, self._robots_pos[i])

        return playground


def print_keyboard_man():
    print("How to use the keyboard to direct the robot?")
    print("\t- up / down key : forward and backward")
    print("\t- left / right key : turn left / right")
    print("\t- shift + left/right key : left/right lateral movement")
    print("\t- g key : grasp objects")
    print("\t- l key : display (or not) the lidar sensor")
    print("\t- s key : display (or not) the semantic sensor")
    print("\t- t key : display (or not) the touch sensor")
    print("\t- q key : exit the program")
    print("\t- r key : reset")


def main():
    print_keyboard_man()
    my_map = MyMapKeyboard()

    playground = my_map.construct_playground(robot_type=MyRobotKeyboard)

    # draw_lidar : enable the visualization of the lidar rays
    # draw_semantic : enable the visualization of the semantic rays
    # draw_touch : enable the visualization of the touch sensor
    gui = GuiSR(playground=playground,
                the_map=my_map,
                draw_lidar=True,
                draw_semantic=True,
                draw_touch=True,
                use_keyboard=True,
                )
    gui.run()


if __name__ == '__main__':
    main()
