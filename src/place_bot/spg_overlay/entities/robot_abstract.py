import math
from abc import abstractmethod
from enum import IntEnum

from spg.agent.agent import Agent

from place_bot.spg_overlay.entities.robot_base import RobotBase
from place_bot.spg_overlay.entities.robot_distance_sensors import RobotLidar
from place_bot.spg_overlay.entities.robot_sensors import RobotOdometer

import matplotlib.pyplot as plt

from place_bot.spg_overlay.utils.utils import normalize_angle


class RobotAbstract(Agent):
    """
    This class should be used as a parent class to create your own Robot class.
    It is a BaseAgent class with 3 sensors, 1 sensor of position and one mandatory functions control()
    """

    class SensorType(IntEnum):
        LIDAR = 0
        ODOMETER = 1

    def __init__(self, should_display_lidar=False):
        super().__init__(interactive=True, lateral=False, radius=10)

        base = RobotBase()
        self.add(base)

        self.base.add(RobotLidar(invisible_elements=self._parts))
        self.base.add(RobotOdometer())

        self._should_display_lidar = should_display_lidar

        if self._should_display_lidar:
            plt.figure(self.SensorType.LIDAR)
            plt.axis([-300, 300, 0, 300])
            plt.ion()

    @abstractmethod
    def control(self):
        """
        This function is mandatory in the class you have to create that will inherit from this class.
        This function should return a command which is a dict with values for the actuators.
        For example:
        command = {"forward": 1.0,
                   "rotation": -1.0}
        """
        pass

    def lidar(self):
        """
        Give access to the value of the lidar sensor.
        """
        return self.sensors[self.SensorType.LIDAR.value]

    def lidar_is_disabled(self):
        return self.lidar().is_disabled()

    # def measured_velocity(self):
    #     """
    #     Give the measured velocity of the robot, in pixels per second
    #     You must use this value for your calculation in the control() function.
    #     """
    #     speed = self.odometer_values()[0]
    #     angle = self.compass_values()
    #     vx = speed * math.cos(angle)
    #     vy = speed * math.sin(angle)
    #     return vx, vy

    def measured_angular_velocity(self):
        """
        Give the measured angular velocity of the robot, in radians per second
        You must use this value for your calculation in the control() function.
        """
        return self.odometer_values()[2]

    def odometer_is_disabled(self):
        return self.sensors[self.SensorType.ODOMETER].is_disabled()

    def odometer_values(self):
        return self.sensors[self.SensorType.ODOMETER].get_sensor_values()

    def true_position(self):
        """
        Give the true orientation of the robot, in pixels
        You must NOT use this value for your calculation in the control() function, you should
        compute an estimated position from odometry values.
        But you can use it for debugging or logging.
        """
        return self.position

    def true_angle(self):
        """
        Give the true orientation of the robot, in radians between 0 and 2Pi.
        You must NOT use this value for your calculation in the control() function, you should
        compute an estimated angle from odometry values.
        But you can use it for debugging or logging.
        """
        return normalize_angle(self.angle)

    def true_velocity(self):
        """
        Give the true velocity of the robot, in pixels per second
        You must NOT use this value for your calculation in the control() function, you should use
        odometry data instead. But you can use it for debugging or logging.
        """
        return self.base.velocity

    def true_angular_velocity(self):
        """
        Give the true angular velocity of the robot, in radians per second
        You must NOT use this value for your calculation in the control() function, you should use
        odometry data instead. But you can use it for debugging or logging.
        """
        return self.base.angular_velocity

    def display(self):
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self):
        if self.lidar().get_sensor_values() is not None:
            plt.figure(self.SensorType.LIDAR)
            plt.cla()
            plt.axis([-math.pi, math.pi, 0, self.lidar().max_range])
            plt.plot(self.lidar().ray_angles, self.lidar().get_sensor_values(), "g.:")
            plt.grid(True)
            plt.draw()
            plt.pause(0.001)
