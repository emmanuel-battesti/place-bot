import math
from abc import abstractmethod

from place_bot.simulation.ray_sensors.lidar import LidarParams
from place_bot.simulation.robot.odometer import OdometerParams
from place_bot.simulation.robot.robot_abstract import RobotAbstract

import pyqtgraph
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication


# Constants for PyQtGraph display configuration
DEFAULT_WINDOW_WIDTH = 600
DEFAULT_WINDOW_HEIGHT = 400
INITIAL_DATA_POINTS = 100  # Placeholder points for initial plot


class RobotAbstractDisplayLidar(RobotAbstract):
    """
    This class should be used as a parent class to create your own Robot class.
    It displays the lidar measurements using PyQtGraph, which is faster than Matplotlib.

    Prerequisites:
        To use this class on Ubuntu/Debian, you need to install:
        sudo apt-get install libxcb-cursor0 libxcb-cursor-dev

        You may also need:
        sudo apt-get install libxcb-xinerama0 libxcb-xinerama-dev libxkbcommon-x11-0

    Args:
        should_display_lidar (bool): Enable/disable lidar visualization window.
        lidar_params (LidarParams): Configuration parameters for the lidar sensor.
        odometer_params (OdometerParams): Configuration parameters for the odometer sensor.
    """

    def __init__(self,
                 should_display_lidar: bool = False,
                 lidar_params: LidarParams = LidarParams(),
                 odometer_params: OdometerParams = OdometerParams()):
        super().__init__(lidar_params=lidar_params,
                         odometer_params=odometer_params)

        self._should_display_lidar = should_display_lidar

        if self._should_display_lidar:
            # Use existing QApplication instance if available, otherwise create one
            self._app = QApplication.instance()
            if self._app is None:
                self._app = QApplication([])

            # Create the visualization window
            self._win = pyqtgraph.GraphicsLayoutWidget(title="Lidar Measurements")
            self._win.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

            # Create the plot with proper labels and ranges
            self._plot = self._win.addPlot(title="Lidar measurements")
            self._plot.setLabel('left', 'Distance (pixels)')
            self._plot.setLabel('bottom', 'Angle (rad)')
            self._plot.setXRange(-math.pi, math.pi)
            self._plot.setYRange(0, lidar_params.max_range)

            # Initialize with placeholder data
            angles = [0] * INITIAL_DATA_POINTS
            distances = [0] * INITIAL_DATA_POINTS
            self._curve = self._plot.plot(angles, distances, pen='g', symbol='o')
            self._win.show()

    def display(self) -> None:
        """
        Display the lidar data if visualization is enabled.

        This method is called to update the PyQtGraph display window.
        It should be called after each simulation step to refresh the visualization.
        """
        if self._should_display_lidar:
            self.display_lidar()

    def display_lidar(self) -> None:
        """
        Update the lidar visualization with current sensor data.

        Plots the lidar angles and distances in the PyQtGraph window.
        If sensor values are not yet available, the display is not updated.
        """
        sensor_values = self.lidar().get_sensor_values()
        if sensor_values is not None:
            angles = self.lidar().get_ray_angles()
            # Validate data consistency
            if len(angles) == len(sensor_values):
                self._curve.setData(angles, sensor_values)
                QCoreApplication.processEvents()
            else:
                # This should not happen, but log a warning if it does
                print(f"Warning: Lidar angles ({len(angles)}) and distances ({len(sensor_values)}) size mismatch")

    @abstractmethod
    def control(self):
        """
        Define the control command for the robot.

        This method must be implemented by subclasses.

        Returns:
            CommandsDict: Dictionary containing 'forward' and 'rotation' commands.
        """
        pass

