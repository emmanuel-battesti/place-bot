"""
This program can be launched directly.
To move the robot, you have to click on the world, then use the arrows on the
keyboard
"""

import os
import sys

from spg.playground.playground import CommandsDict

# This line add, to sys.path, the path to parent path of this file
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worlds.walls_complete_world_2 import add_walls, add_boxes
# from place_bot.old_entities.robot_abstract_display_lidar_v1 import RobotAbstractDisplayLidarV1
from place_bot.simulation.robot.robot_abstract_display_lidar_v2 import RobotAbstractDisplayLidarV2
from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.old_simu_world import ClosedPlayground
from place_bot.simulation.old_simu_world.simulator import Simulator
from place_bot.simulation.old_simu_world import WorldAbstract


class MyRobotLidar(RobotAbstractDisplayLidarV2):
    def control(self) -> CommandsDict:
        """
        We only send a command to do nothing
        """
        command: CommandsDict = {"forward": 0.0,
                   "rotation": 0.0}
        return command


class MyWorldLidar(WorldAbstract):

    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (1113, 750)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)
        add_walls(self._playground)
        add_boxes(self._playground)

        # POSITION OF THE ROBOT
        self._robot_pos = ((-50, 0), 0)
        self._playground.add(robot, self._robot_pos)


def main():
    my_robot = MyRobotLidar(should_display_lidar=True)
    my_world = MyWorldLidar(robot=my_robot)

    # draw_lidar_rays : enable the visualization of the lidar rays
    # enable_visu_noises : to enable the visualization. It will show also a demonstration of the integration
    # of odometer values, by drawing the estimated path in red.
    simulator = Simulator(the_world=my_world,
                          draw_lidar_rays=True,
                          use_keyboard=True,
                          enable_visu_noises=True,
                          )
    simulator.run()

if __name__ == '__main__':
    main()
