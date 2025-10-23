import math
from abc import abstractmethod

from place_bot.simulation.entities.lidar import LidarParams
from place_bot.simulation.entities.odometer import OdometerParams
from place_bot.simulation.entities.robot_abstract import RobotAbstract

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class RobotAbstractDisplayLidarV1(RobotAbstract):
    """
    This class should be used as a parent class to create your own Robot class.
    It displays the lidar measurements using Matplotlib.
    """

    def __init__(self,
                 should_display_lidar=False,
                 lidar_params: LidarParams = LidarParams(),
                 odometer_params: OdometerParams = OdometerParams()):
        super().__init__(lidar_params=lidar_params,
                         odometer_params=odometer_params)

        self._should_display_lidar = should_display_lidar

        if self._should_display_lidar:
            plt.figure("Lidar")
            plt.axis([-300, 300, 0, 300])
            plt.title("lidar measurements")
            plt.ion()


    def display(self):
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self):
        if self.lidar().get_sensor_values() is not None:
            plt.figure("Lidar")
            plt.cla()
            plt.axis([-math.pi, math.pi, 0, self.lidar().max_range])
            plt.plot(self.lidar().get_ray_angles(), self.lidar().get_sensor_values(), "g.:")
            plt.grid(True)
            plt.title("lidar measurements", fontsize=16)
            plt.draw()
            plt.pause(0.1)

    @abstractmethod
    def control(self):
        pass
