import math
from abc import abstractmethod

from place_bot.simulation.ray_sensors.lidar import LidarParams
from place_bot.simulation.robot.odometer import OdometerParams
from place_bot.simulation.robot.robot_abstract import RobotAbstract

import pyqtgraph
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication


class RobotAbstractDisplayLidar(RobotAbstract):
    """
    This class should be used as a parent class to create your own Robot class.
    It displays the lidar measurements using PyQtGraph, which is faster than Matplotlib.
    To use this class, you need to install with apt:
    sudo apt-get install libxcb-cursor0 libxcb-cursor-dev
    and maybe also:
    sudo apt-get install libxcb-xinerama0 libxcb-xinerama-dev libxkbcommon-x
    """

    def __init__(self,
                 should_display_lidar=False,
                 lidar_params: LidarParams = LidarParams(),
                 odometer_params: OdometerParams = OdometerParams()):
        super().__init__(lidar_params=lidar_params,
                         odometer_params=odometer_params)

        self._should_display_lidar = should_display_lidar

        if self._should_display_lidar:
            self._app = QApplication.instance()  # Use QApplication directly
            if self._app is None:
                self._app = QApplication([])
            self._win = pyqtgraph.GraphicsLayoutWidget(title="Lidar Measurements")
            self._win.resize(600, 400)
            self._plot = self._win.addPlot(title="Lidar measurements")
            self._plot.setLabel('left', 'Distance')
            self._plot.setLabel('bottom', 'Angle (rad)')
            self._plot.setXRange(-math.pi, math.pi)
            self._plot.setYRange(0, lidar_params.max_range)
            angles = [0] * 100  # Exemple : 100 points avec des angles à 0
            distances = [0] * 100  # Exemple : 100 points avec des distances à 0
            self._curve = self._plot.plot(angles, distances, pen='g', symbol='o')
            self._win.show()

    def display(self):
        """
        Display the lidar data if visualization is enabled.
        This method is called to update the PyQtGraph display window.
        """
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self):
        """
        Update the lidar visualization with current sensor data.
        Plots the lidar angles and distances in the PyQtGraph window.
        """
        if self.lidar().get_sensor_values() is not None:
            angles = self.lidar().get_ray_angles()
            distances = self.lidar().get_sensor_values()
            self._curve.setData(angles, distances)
            QCoreApplication.processEvents()

    @abstractmethod
    def control(self):
        pass

