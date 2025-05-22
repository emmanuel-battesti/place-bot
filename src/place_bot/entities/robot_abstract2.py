import math
from abc import abstractmethod
from enum import IntEnum

from spg.agent.agent import Agent

from place_bot.entities.robot_base import RobotBase
from place_bot.entities.lidar import Lidar, LidarParams
# from place_bot.entities.odometer import Odometer
# from place_bot.entities.odometer_v2 import OdometerV2
from place_bot.entities.odometer import Odometer, OdometerParams
from place_bot.utils.utils import normalize_angle

import pyqtgraph
from pyqtgraph.Qt import QtCore, QtWidgets


class RobotAbstract2(Agent):
    """
    This class should be used as a parent class to create your own Robot class.
    It is a BaseAgent class with 3 sensors, 1 sensor of position and one mandatory functions control()
    """

    class SensorType(IntEnum):
        LIDAR = 0
        ODOMETER = 1

    def __init__(self,
                 should_display_lidar=False,
                 lidar_params: LidarParams = LidarParams(),
                 odometer_params: OdometerParams = OdometerParams()):
        super().__init__(interactive=True, lateral=False, radius=10)

        base = RobotBase()
        self.add(base)

        self.base.add(Lidar(lidar_params=lidar_params, invisible_elements=self._parts))
        self.base.add(Odometer(odometer_params=odometer_params))

        self._should_display_lidar = should_display_lidar

        if self._should_display_lidar:
            self._app = QtWidgets.QApplication.instance()  # Use QtWidgets.QApplication
            if self._app is None:
                self._app = QtWidgets.QApplication([])
            self._win = pyqtgraph.GraphicsLayoutWidget(title="Lidar Measurements")
            self._win.resize(600, 400)
            self._plot = self._win.addPlot(title="Lidar measurements")
            self._plot.setLabel('left', 'Distance')
            self._plot.setLabel('bottom', 'Angle (rad)')
            self._plot.setXRange(-math.pi, math.pi)
            self._plot.setYRange(0, lidar_params.max_range)
            self._curve = self._plot.plot(pen='g', symbol='o')
            self._win.show()
            angles = [0] * 100  # Exemple : 100 points avec des angles à 0
            distances = [0] * 100  # Exemple : 100 points avec des distances à 0
            self._curve = self._plot.plot(angles, distances, pen='g', symbol='o')

    @abstractmethod
    def control(self):
        """
        This function is mandatory in the class you have to create that will
        inherit from this class.
        This function should return a command which is a dict with values for
        the actuators.
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

    def odometer_is_disabled(self):
        return self.sensors[self.SensorType.ODOMETER].is_disabled()

    def odometer_values(self):
        """
        Give the estimated pose after integration of odometer's delta
        """
        return self.sensors[self.SensorType.ODOMETER].get_sensor_values()

    def true_position(self):
        """
        Give the true orientation of the robot, in pixels
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return self.position

    def true_angle(self):
        """
        Give the true orientation of the robot, in radians between 0 and 2Pi.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return normalize_angle(self.angle)

    def true_velocity(self):
        """
        Give the true velocity of the robot, in pixels per second
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return self.base.velocity

    def true_angular_velocity(self) -> float:
        """
        Give the true angular velocity of the robot, in radians per second
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return self.base.angular_velocity

    def display(self):
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self):
        if self.lidar().get_sensor_values() is not None:
            angles = self.lidar().get_ray_angles()
            distances = self.lidar().get_sensor_values()
            self._curve.setData(angles, distances)
            QtCore.QCoreApplication.processEvents()
