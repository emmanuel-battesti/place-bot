import math
from abc import abstractmethod
from enum import IntEnum

from spg.agent.agent import Agent

from place_bot.entities.robot_base import RobotBase
from place_bot.entities.lidar import Lidar, LidarParams
from place_bot.entities.odometer import Odometer, OdometerParams
from place_bot.utils.utils import normalize_angle
from place_bot.entities.robot_abstract import RobotAbstract

import pyqtgraph
# from pyqtgraph.Qt import QtCore, QtWidgets
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

class RobotAbstractDisplayLidarV2(RobotAbstract):
    """
    This class should be used as a parent class to create your own Robot class.
    It displays the lidar measurements using PyQtGraph, which is a faster than Matplotlib.
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
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self):
        if self.lidar().get_sensor_values() is not None:
            angles = self.lidar().get_ray_angles()
            distances = self.lidar().get_sensor_values()
            self._curve.setData(angles, distances)
            QCoreApplication.processEvents()

    @abstractmethod
    def control(self):
        pass
