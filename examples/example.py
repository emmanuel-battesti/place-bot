from place_bot.simulation.gui_map.simulator import Simulator

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
