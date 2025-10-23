from place_bot.simulation.old_entities.robot_abstract import RobotAbstract
from place_bot.simulation.simu_world.simulator import Simulator

from worlds.world_intermediate_01 import MyWorldIntermediate01
from worlds.world_complete_01 import MyWorldComplete01
from worlds.world_complete_02 import MyWorldComplete02


class MyWorld(MyWorldComplete02):
    pass


class MyRobot(RobotAbstract):
    """
    Dummy robot class for world checking.
    """

    def control(self) -> CommandsDict:
        pass


def main():
    """
    Runs a GUI to check the world visually with a dummy robot.
    """
    my_robot = MyRobot
    my_world = MyWorld(robot=my_robot)

    simulator = Simulator(the_world=my_world,
                          use_mouse_measure=True)

    simulator.run()

if __name__ == '__main__':
    main()