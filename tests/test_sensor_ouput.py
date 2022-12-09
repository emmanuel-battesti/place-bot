import math

import numpy as np
import pymunk
import pytest

from typing import Optional, List, Type

from place_bot.entities.robot_abstract import RobotAbstract
from place_bot.gui_map.closed_playground import ClosedPlayground
from place_bot.gui_map.gui_sr import GuiSR
from place_bot.gui_map.map_abstract import MapAbstract


class MyRobot(RobotAbstract):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def control(self):
        command = {"forward": 1.0,
                   "rotation": 0.0}
        return command


class MyWorld(MapAbstract):
    def __init__(self, robot: RobotAbstract):
        super().__init__(robot=robot)

        # PARAMETERS MAP
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
    my_map = MyWorld(robot=my_robot)

    robots_commands = {}
    for _ in range(100):
        command = my_map.robot.control()
        robots_commands[my_map.robot] = command
        my_map._playground.step(commands=robots_commands)

    moved = my_map._playground.agents[0].true_position() != (0, 0)

    assert moved is True


def test_lidar():
    """
    Check values of the lidar
    """
    my_robot = MyRobot()
    my_map = MyWorld(robot=my_robot)

    playground = my_map._playground

    for _ in range(1):
        playground.step()

    ok = True
    if my_map.robot.lidar().get_sensor_values() is None:
        ok = False

    w, h = my_map.size_area
    max_dist_theoretical = math.sqrt(w * w + h * h) / 2
    min_dist_theoretical = min(w, h) / 2

    max_dist = max(my_map.robot.lidar().get_sensor_values())
    min_dist = min(my_map.robot.lidar().get_sensor_values())
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
    my_map = MyWorld(robot=my_robot)

    playground = my_map._playground

    ok = True
    if my_map.robot.lidar().get_sensor_values() is None:
        ok = False

    val = max(my_map.robot.lidar().get_sensor_values())

    assert ok is True and np.isnan(val)


def test_positions():
    """
    Check values of the gps sensor
    """
    my_robot = MyRobot()
    my_map = MyWorld(robot=my_robot)

    playground = my_map._playground

    for _ in range(1):
        playground.step()

    # -- ODOMETER -- #
    odometer_array = my_map.robot.odometer_values()
    # odometer_array = array([-0.13856926, -0.01582876, -0.01264697])
    assert odometer_array is not None
    assert type(odometer_array) is np.ndarray

    # -- TRUE POSITION -- #
    true_pos = my_map.robot.true_position()
    # true_pos = Vec2d(12.3, 456.78)
    assert true_pos is not None
    assert type(true_pos) is pymunk.vec2d.Vec2d

    # -- TRUE ANGLE -- #
    true_angle = my_map.robot.true_angle()
    # true_angle = 1.2345
    assert true_angle is not None
    assert type(true_angle) is float


def test_positions_nan():
    """
    Check values of the gps sensor
    """
    my_robot = MyRobot()
    my_map = MyWorld(robot=my_robot)

    playground = my_map._playground

    # -- ODOMETER -- #
    odometer_array = my_map.robot.odometer_values()
    # odometer_array = array([-0.13856926, -0.01582876, -0.01264697])
    assert odometer_array is not None
    assert type(odometer_array) is np.ndarray

    # -- TRUE ANGLE -- #
    true_angle = my_map.robot.true_angle()
    # true_angle = nan
    assert not np.isnan(true_angle)
    assert true_angle is not None
    assert type(true_angle) is float
