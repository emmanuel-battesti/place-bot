from abc import abstractmethod
from enum import IntEnum
import numpy as np
from PySide6.QtCore import QCoreApplication

from place_bot.simulation.robot.agent import Agent
from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_base import RobotBase
from place_bot.simulation.ray_sensors.lidar import Lidar, LidarParams
from place_bot.simulation.robot.odometer import Odometer, OdometerParams
from place_bot.simulation.utils.utils import normalize_angle


class RobotAbstract(Agent):
    """
    Abstract base class for robot in the simulation.

    This class should be used as a parent class to create your own Robot classes.
    It inherits from the Agent class and provides
    functionality for controlling a robot in a simulated environment.
    It is a BaseAgent class with 3 sensors, 1 sensor of position and 2
    mandatory functions define_message() and control().

    Example Usage
        # Create a custom Robot class that inherits from RobotAbstract
        class MyRobot(RobotAbstract):
            def control(self) -> CommandsDict:
                # Define the control command for the robot
                command = {"forward": 1.0, "rotation": -1.0,
                }
                return command

        # Create an instance of the custom robot class
        robot = MyRobot()

        # Access sensor values and other functionalities
        lidar_values = robot.lidar()

        # Control the robot
        command = robot.control()

     Attributes:
        identifier (int): The identifier of the robot.
        _should_display_lidar_graph (bool): Whether to display lidar data with matplotlib.
        size_area (tuple): The size of the area in which the robot operates.
        _timer_collision_wall_or_robot (Timer): Timer for collision events.
        elapsed_timestep (int): Number of timesteps since the beginning.
        elapsed_walltime (float): Elapsed wall time in seconds since the beginning.
    """

    class SensorType(IntEnum):
        """
        Enumeration of sensor types for the robot.
        """
        LIDAR = 0
        ODOMETER = 1

    def __init__(
            self,
            lidar_params: LidarParams = LidarParams(),
            odometer_params: OdometerParams = OdometerParams(),
            display_lidar_graph: bool = False):
        """
        Initialize the RobotAbstract.
        """
        super().__init__(interactive=True, lateral=False, radius=10)

        self.add_base(RobotBase())

        self.base.add_device(Lidar(lidar_params=lidar_params, invisible_elements=self.base))
        self.base.add_device(Odometer(odometer_params=odometer_params))

        self._should_display_lidar_graph = display_lidar_graph

    @abstractmethod
    def control(self) -> CommandsDict:
        """
        This function is mandatory in the class you have to create that will
        inherit from this class.
        Define the control command for the robot.
        For example:
        command = {"forward": 1.0,
                   "rotation": -1.0}
        Returns:
            CommandsDict: Dictionary of actuator commands.
        """
        pass

    def lidar(self):
        """
        Access the lidar sensor.

        Returns:
            RobotLidar: The lidar sensor.
        """
        return self.sensors[self.SensorType.LIDAR.value]

    def lidar_is_disabled(self) -> bool:
        """
        Returns whether the lidar sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self.lidar().is_disabled()

    def odometer_is_disabled(self) -> bool:
        """
        Returns whether the odometer sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self.sensors[self.SensorType.ODOMETER].is_disabled()

    def lidar_values(self):
        """
        Get the current values from the lidar sensor.

        Returns:
            Any: Sensor values.
        """
        return self.lidar().get_sensor_values()

    def lidar_rays_angles(self):
        """
        Get the angles of the lidar rays.

        Returns:
            Any: Ray angles.
        """
        return self.lidar().get_ray_angles()

    def odometer_values(self):
        """
        Give the estimated pose after integration of odometer's delta
        """
        return self.sensors[self.SensorType.ODOMETER].get_sensor_values()

    @property
    def position(self):
        """
        Disabled: Use measured_gps_position() instead.
        """
        raise Exception('Function Disabled')

    @property
    def angle(self):
        """
        Disabled: Use measured_compass_angle() instead.
        """
        raise Exception('Function Disabled')

    @property
    def velocity(self):
        """
        Disabled: Use measured_velocity() instead.
        """
        raise Exception('Function Disabled')

    @property
    def angular_velocity(self):
        """
        Disabled: Use measured_angular_velocity() instead.
        """
        raise Exception('Function Disabled')

    def true_position(self) -> np.ndarray:
        """
        Get the true position of the robot, in pixels.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        Returns:
            np.ndarray: The true position.
        """
        return np.array(self.base._pm_body.position)

    def true_angle(self) -> float:
        """
        Get the true orientation of the robot, in radians between 0 and 2Pi.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return normalize_angle(self.base._pm_body.angle)

    def true_velocity(self) -> np.ndarray:
        """
        Get the true velocity of the robot in 2D, in pixels per second
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return np.array(self.base._pm_body.velocity)

    def true_angular_velocity(self) -> float:
        """
        Get the true angular velocity of the robot, in radians per second
        You must NOT use this value for your calculation in the control() function, instead you
        should use the position estimated by the odometer sensor.
        But you can use it for debugging or logging.
        """
        return self.base._pm_body.angular_velocity

    def display(self) -> None:
        """
        Display lidar graph if enabled.
        """
        if self._should_display_lidar_graph:
            self.display_lidar_graph()

    def display_lidar_graph(self) -> None:
        """
        Display the lidar sensor data using matplotlib.
        """
        if self.lidar_values() is not None:
            angles = self.lidar().get_ray_angles()
            distances = self.lidar().get_sensor_values()
            self._curve.setData(angles, distances)
            QCoreApplication.processEvents()

    def draw_bottom_layer(self) -> None:
        """
        Draw elements on the bottom layer (override as needed).
        """
        pass

    def draw_top_layer(self) -> None:
        """
        Draw elements on the top layer (override as needed).
        """
        pass

    def pre_step(self) -> None:
        """
        Prepare the robot for a new simulation step.
        """
        super().pre_step()
