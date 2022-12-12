from place_bot.utils.screen_recorder import ScreenRecorder
from place_bot.simu_world.simulator import Simulator

from worlds.world_intermediate_01 import MyWorldIntermediate01
from worlds.world_complete_01 import MyWorldComplete01
from worlds.world_complete_02 import MyWorldComplete02


from robots.my_robot_random import MyRobotRandom


class MyWorld(MyWorldComplete02):
    pass


class MyRobot(MyRobotRandom):
    pass


if __name__ == "__main__":
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)
    simulator = Simulator(the_world=my_world)
    simulator.run()
