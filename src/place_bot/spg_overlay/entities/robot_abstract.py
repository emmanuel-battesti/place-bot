import math
from abc import abstractmethod
from enum import IntEnum
from typing import Optional

from spg.agent.agent import Agent

from spg_overlay.entities.robot_base import RobotBase
from spg_overlay.entities.robot_distance_sensors import RobotLidar, RobotTouch, RobotSemanticSensor
from spg_overlay.entities.robot_sensors import RobotGPS, RobotCompass, RobotOdometer
from spg_overlay.utils.misc_data import MiscData

import matplotlib.pyplot as plt

from spg_overlay.utils.utils import normalize_angle


class RobotAbstract(Agent):
    """
    This class should be used as a parent class to create your own Robot class.
    It is a BaseAgent class with 3 sensors, 1 sensor of position and one mandatory functions control()
    """

    class SensorType(IntEnum):
        TOUCH = 0
        SEMANTIC = 1
        LIDAR = 2
        GPS = 3
        COMPASS = 4
        ODOMETER = 5

    def __init__(self,
                 identifier: Optional[int] = None,
                 misc_data: MiscData = None,
                 should_display_lidar=False,
                 should_display_touch=False,
                 **kwargs
                 ):
        super().__init__(interactive=True, lateral=False, radius=10, **kwargs)

        if identifier is None:
            identifier = id(self)

        base = RobotBase()
        self.add(base)

        self.size_area = None
        if misc_data:
            self.size_area = misc_data.size_area

        self.base.add(RobotTouch(invisible_elements=self._parts))
        self.base.add(RobotSemanticSensor(playground=self.playground, invisible_elements=self._parts))
        self.base.add(RobotLidar(invisible_elements=self._parts))

        self.base.add(RobotGPS())
        self.base.add(RobotCompass())
        self.base.add(RobotOdometer())

        self.identifier = identifier
        self._should_display_lidar = should_display_lidar
        self._should_display_touch = should_display_touch

        if self._should_display_lidar:
            plt.figure(self.SensorType.LIDAR)
            plt.axis([-300, 300, 0, 300])
            plt.ion()

        if self._should_display_touch:
            plt.figure(self.SensorType.TOUCH)
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

    def touch(self):
        """
        Give access to the value of the touch sensor.
        """
        return self.sensors[self.SensorType.TOUCH.value]

    def semantic(self):
        """
        Give access to the value of the semantic sensor.
        """
        return self.sensors[self.SensorType.SEMANTIC.value]

    def lidar(self):
        """
        Give access to the value of the lidar sensor.
        """
        return self.sensors[self.SensorType.LIDAR.value]

    def touch_is_disabled(self):
        return self.touch().is_disabled()

    def semantic_is_disabled(self):
        return self.semantic().is_disabled()

    def lidar_is_disabled(self):
        return self.lidar().is_disabled()

    def measured_velocity(self):
        """
        Give the measured velocity of the robot, in pixels per second
        You must use this value for your calculation in the control() function.
        """
        speed = self.odometer_values()[0]
        angle = self.compass_values()
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        return vx, vy

    def measured_angular_velocity(self):
        """
        Give the measured angular velocity of the robot, in radians per second
        You must use this value for your calculation in the control() function.
        """
        return self.odometer_values()[2]

    def measured_gps_position(self):
        """
        Give the measured position of the robot, in pixels. The measurement comes from the GPS sensor.
        You can use this value for your calculation in the control() function. These values can be altered
        by special areas in the map where the position information can be scrambled.
        """
        if self.sensors[self.SensorType.GPS].is_disabled():
            return None

        return self.sensors[self.SensorType.GPS].get_sensor_values()[0], \
               self.sensors[self.SensorType.GPS].get_sensor_values()[1]

    def measured_compass_angle(self):
        """
        Give the measured orientation of the robot, in radians between 0 and 2Pi. The measurement comes from the compass
        sensor. You can use this value for your calculation in the control() function. These values can be altered
        by special areas in the map where the position information can be scrambled.
        """
        if self.sensors[self.SensorType.COMPASS].is_disabled():
            return None

        return self.sensors[self.SensorType.COMPASS].get_sensor_values()[0]

    def gps_is_disabled(self):
        return self.sensors[self.SensorType.GPS].is_disabled()

    def compass_is_disabled(self):
        return self.sensors[self.SensorType.COMPASS].is_disabled()

    def odometer_is_disabled(self):
        return self.sensors[self.SensorType.ODOMETER].is_disabled()

    def odometer_values(self):
        return self.sensors[self.SensorType.ODOMETER].get_sensor_values()

    def gps_values(self):
        return self.sensors[self.SensorType.GPS].get_sensor_values()

    def compass_values(self):
        return self.sensors[self.SensorType.COMPASS].get_sensor_values()

    def true_position(self):
        """
        Give the true orientation of the robot, in pixels
        You must NOT use this value for your calculation in the control() function, you should use measured_gps_position()
        instead. But you can use it for debugging or logging.
        """
        return self.position

    def true_angle(self):
        """
        Give the true orientation of the robot, in radians between 0 and 2Pi.
        You must NOT use this value for your calculation in the control() function, you should use measured_compass_angle()
        instead. But you can use it for debugging or logging.
        """
        return normalize_angle(self.angle)

    def true_velocity(self):
        """
        Give the true velocity of the robot, in pixels per second
        You must NOT use this value for your calculation in the control() function, you should use GPS, Compass or
        odometry data instead. But you can use it for debugging or logging.
        """
        return self.base.velocity

    def true_angular_velocity(self):
        """
        Give the true angular velocity of the robot, in radians per second
        You must NOT use this value for your calculation in the control() function, you should use GPS, Compass or
        odometry data instead. But you can use it for debugging or logging.
        """
        return self.base.angular_velocity

    def display(self):
        if self._should_display_lidar:
            self.display_lidar()
        if self._should_display_touch:
            self.display_touch()

    def display_lidar(self):
        if self.lidar().get_sensor_values() is not None:
            plt.figure(self.SensorType.LIDAR)
            plt.cla()
            plt.axis([-math.pi, math.pi, 0, self.lidar().max_range])
            plt.plot(self.lidar().ray_angles, self.lidar().get_sensor_values(), "g.:")
            plt.grid(True)
            plt.draw()
            plt.pause(0.001)

    def display_touch(self):
        if self.touch().get_sensor_values() is not None:
            plt.figure(self.SensorType.TOUCH)
            plt.cla()
            plt.axis([-math.pi / 2, math.pi / 2, 0, 1])
            plt.plot(self.touch().ray_angles, self.touch().get_sensor_values(), "g.:")
            plt.grid(True)
            plt.draw()
            plt.pause(0.001)
