import math

import numpy as np
import pymunk

from typing import Type

from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.old_simu_world import ClosedPlayground
from place_bot.simulation.old_simu_world import WorldAbstract


class MyRobot(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def control(self):
        command = {"forward": 1.0,
                   "rotation": 0.0}
        return command


class MyWorld(WorldAbstract):
    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS WORLD
        self._size_area = (200, 200)

        # PLAYGROUND
        self._playground = ClosedPlayground(size=self._size_area)

        # POSITIONS OF THE ROBOT
        self._robot_pos = ((0, 0), 0)
        # robot.init_pose(self._robot_pos[0][0],self._robot_pos[0][1],self._robot_pos[1])
        self._playground.add(robot, self._robot_pos)

    def construct_playground(self, robot_type: Type[RobotAbstract]):
        playground = ClosedPlayground(size=self._size_area)

        # POSITIONS OF THE ROBOTS
        robot = robot_type()
        playground.add(robot, self._robot_pos)

        return playground


def test_move():
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)

    robots_commands = {}
    for _ in range(100):
        command = my_world.robot.control()
        robots_commands[my_world.robot] = command
        my_world._playground.step(commands=robots_commands)

    moved = my_world._playground.agents[0].true_position() != (0, 0)

    assert moved is True


def test_lidar():
    """
    Check values of the lidar
    """
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)

    playground = my_world._playground

    for _ in range(1):
        playground.step()

    ok = True
    if my_world.robot.lidar().get_sensor_values() is None:
        ok = False

    w, h = my_world.size_area
    max_dist_theoretical = math.sqrt(w * w + h * h) / 2
    min_dist_theoretical = min(w, h) / 2

    max_dist = max(my_world.robot.lidar().get_sensor_values())
    min_dist = min(my_world.robot.lidar().get_sensor_values())
    # print("half_diag = ", half_diag)
    # print("max_dist = ", max_dist)

    assert ok is True
    assert max_dist < (max_dist_theoretical + 20)
    assert max_dist > (max_dist_theoretical - 20)
    assert min_dist > (min_dist_theoretical - 20)
    assert min_dist < (min_dist_theoretical + 20)


def test_lidar_nan():
    """
    Here, we dont use the step function of playground
    So, we don't have lidar value.
    """
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)

    playground = my_world._playground

    ok = True
    if my_world.robot.lidar().get_sensor_values() is None:
        ok = False

    val = max(my_world.robot.lidar().get_sensor_values())

    assert ok is True and np.isnan(val)


def test_positions():
    """
    Check values of the gps sensor
    """
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)

    playground = my_world._playground

    for _ in range(1):
        playground.step()

    # -- ODOMETER -- #
    odometer_array = my_world.robot.odometer_values()
    # odometer_array = array([138.56926, 158.2876, -0.01264697])
    assert odometer_array is not None
    assert type(odometer_array) is np.ndarray

    # -- TRUE POSITION -- #
    true_pos = my_world.robot.true_position()
    # true_pos = Vec2d(12.3, 456.78)
    assert true_pos is not None
    assert type(true_pos) is pymunk.vec2d.Vec2d

    # -- TRUE ANGLE -- #
    true_angle = my_world.robot.true_angle()
    # true_angle = 1.2345
    assert true_angle is not None
    assert type(true_angle) is float


def test_positions_nan():
    """
    Check values of the gps sensor
    """
    my_robot = MyRobot()
    my_world = MyWorld(robot=my_robot)

    playground = my_world._playground

    # -- ODOMETER -- #
    odometer_array = my_world.robot.odometer_values()
    # odometer_array = array([138.56926, 158.2876, -0.01264697])
    assert odometer_array is not None
    assert type(odometer_array) is np.ndarray

    # -- TRUE POSITION -- #
    true_pos = my_world.robot.true_position()
    # true_pos = Vec2d(12.3, 456.78)
    assert true_pos is not None
    assert type(true_pos) is pymunk.vec2d.Vec2d

    # -- TRUE ANGLE -- #
    true_angle = my_world.robot.true_angle()
    # true_angle = nan
    assert not np.isnan(true_angle)
    assert true_angle is not None
    assert type(true_angle) is float
