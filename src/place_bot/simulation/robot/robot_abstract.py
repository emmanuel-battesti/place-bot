from abc import abstractmethod
from enum import IntEnum
from typing import Optional

import numpy as np

from place_bot.simulation.robot.agent import Agent
from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_base import RobotBase
from place_bot.simulation.ray_sensors.lidar import Lidar, LidarParams
from place_bot.simulation.robot.odometer import Odometer, OdometerParams
from place_bot.simulation.robot.exceptions import DisabledFunctionError
from place_bot.simulation.utils.constants import ROBOT_DEFAULT_RADIUS, FRAME_RATE
from place_bot.simulation.utils.utils import normalize_angle


class RobotAbstract(Agent):
    """
    Abstract base class for robot in the simulation.

    This class should be used as a parent class to create your own Robot classes.
    It inherits from the Agent class and provides functionality for controlling
    a robot in a simulated environment.

    The robot is equipped with two sensors:
    - Lidar: for distance measurements in multiple directions
    - Odometer: for position estimation based on movement

    You must implement the abstract method control() to define robot behavior.

    Example Usage:
        # Create a custom Robot class that inherits from RobotAbstract
        class MyRobot(RobotAbstract):
            def control(self) -> CommandsDict:
                # Define the control command for the robot
                command = {"forward": 1.0, "rotation": -1.0}
                return command

        # Create an instance of the custom robot class
        robot = MyRobot()

        # Access sensor values and other functionalities
        lidar_values = robot.lidar_values()
        odometer_values = robot.odometer_values()

        # Control the robot
        command = robot.control()
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
            odometer_params: OdometerParams = OdometerParams()):
        """
        Initialize the RobotAbstract.

        Args:
            lidar_params (LidarParams): Parameters for the lidar sensor.
            odometer_params (OdometerParams): Parameters for the odometer sensor.
        """
        super().__init__(interactive=True, lateral=False, radius=ROBOT_DEFAULT_RADIUS)

        self.add_base(RobotBase())

        self.base.add_device(Lidar(lidar_params=lidar_params, invisible_elements=self.base))
        self.base.add_device(Odometer(odometer_params=odometer_params))


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

    def lidar(self) -> Lidar:
        """
        Access the lidar sensor.

        Returns:
            Lidar: The lidar sensor instance.
        """
        return self.sensors[self.SensorType.LIDAR.value]

    def lidar_is_disabled(self) -> bool:
        """
        Check whether the lidar sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self.lidar().is_disabled()

    def odometer_is_disabled(self) -> bool:
        """
        Check whether the odometer sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self.sensors[self.SensorType.ODOMETER].is_disabled()

    def lidar_values(self) -> Optional[np.ndarray]:
        """
        Get the current distance values from the lidar sensor.

        Returns:
            Optional[np.ndarray]: Array of distance measurements, or None if sensor is disabled.
        """
        return self.lidar().get_sensor_values()

    def lidar_rays_angles(self) -> np.ndarray:
        """
        Get the angles of the lidar rays.

        Returns:
            np.ndarray: Array of ray angles in radians.
        """
        return self.lidar().get_ray_angles()

    def odometer_values(self) -> Optional[np.ndarray]:
        """
        Get the odometer integrated position estimate.

        The odometer integrates noisy displacement measurements over time to provide
        an estimated position since the robot's starting point. This is dead reckoning:
        the cumulative error grows over time as movements are integrated.

        Returns:
            Optional[np.ndarray]: Array containing [x, y, orientation] where:
                - x (float): Estimated x position in pixels from starting point
                - y (float): Estimated y position in pixels from starting point
                - orientation (float): Estimated orientation in radians (-π to π) from starting orientation
                Returns None if sensor is disabled.

        Note:
            This returns the INTEGRATED position estimate, not raw displacement values.
            The position estimate accumulates errors over time (dead reckoning drift).

        Example:
            >>> pose = robot.odometer_values()
            >>> x, y, orientation = pose
            >>> print(f"Estimated at ({x:.1f}, {y:.1f}), facing {orientation:.2f} rad")
        """
        return self.sensors[self.SensorType.ODOMETER].get_sensor_values()

    def odometer_last_displacement(self) -> tuple[float, float, float]:
        """
        Get the last raw displacement values from the odometer (for debugging).

        This method provides access to the raw displacement values before integration.
        Useful for debugging or understanding the incremental movements.

        Returns:
            tuple[float, float, float]: Tuple containing:
                - dist (float): Distance traveled during last timestep (in pixels)
                - alpha (float): Relative angle in previous robot frame (in radians)
                - theta (float): Orientation change during last timestep (in radians)

        Note:
            These are the noisy raw values, not the integrated position.
            For the integrated position estimate, use odometer_values() instead.
        """
        return self.sensors[self.SensorType.ODOMETER].get_last_displacement()

    def estimated_linear_speed(self) -> float:
        """
        Get the estimated linear speed from the odometer.

        This method calculates the linear speed based on the distance traveled
        during the last timestep as measured by the odometer.

        Returns:
            float: Estimated linear speed in pixels per timestep.
                   Returns 0.0 if odometer is disabled.

        Note:
            This is an estimation based on noisy odometer data.
            The value is in pixels/timestep (not pixels/second).
            To convert to pixels/second, multiply by (1/FRAME_RATE).

        Example:
            >>> speed = robot.estimated_linear_speed()
            >>> print(f"Speed: {speed:.2f} pixels/timestep")
        """
        if not self.odometer_is_disabled():
            dist, alpha, theta = self.odometer_last_displacement()
            return dist
        return 0.0

    def estimated_angular_speed(self) -> float:
        """
        Get the estimated angular speed from the odometer.

        This method calculates the angular speed based on the orientation change
        during the last timestep as measured by the odometer.

        Returns:
            float: Estimated angular speed in radians per timestep.
                   Returns 0.0 if odometer is disabled.

        Note:
            This is an estimation based on noisy odometer data.
            The value is in radians/timestep (not radians/second).
            To convert to radians/second, multiply by (1/FRAME_RATE).
            Positive values indicate counter-clockwise rotation.

        Example:
            >>> angular_speed = robot.estimated_angular_speed()
            >>> print(f"Angular speed: {angular_speed:.3f} rad/timestep")
        """
        if not self.odometer_is_disabled():
            dist, alpha, theta = self.odometer_last_displacement()
            return theta
        return 0.0

    def estimated_velocity(self) -> tuple[float, float]:
        """
        Get the estimated velocity (linear and angular) from the odometer.

        This is a convenience method that returns both linear and angular speeds.

        Returns:
            tuple[float, float]: Tuple containing:
                - linear_speed (float): Linear speed in pixels per timestep
                - angular_speed (float): Angular speed in radians per timestep
                Both return 0.0 if odometer is disabled.

        Note:
            These are estimations based on noisy odometer data.
            Values are per timestep, not per second.

        Example:
            >>> linear, angular = robot.estimated_velocity()
            >>> print(f"Linear: {linear:.2f} px/ts, Angular: {angular:.3f} rad/ts")
        """
        if not self.odometer_is_disabled():
            dist, alpha, theta = self.odometer_last_displacement()
            return (dist, theta)
        return (0.0, 0.0)

    @property
    def position(self):
        """
        Disabled: Use odometer_values() for estimated position or true_position() for debugging.

        Raises:
            DisabledFunctionError: This function is disabled to prevent direct access.
        """
        raise DisabledFunctionError('Function Disabled: Use odometer_values() for estimated position or true_position() for debugging')

    @property
    def angle(self):
        """
        Disabled: Use odometer_values() for estimated orientation or true_angle() for debugging.

        Raises:
            DisabledFunctionError: This function is disabled to prevent direct access.
        """
        raise DisabledFunctionError('Function Disabled: Use odometer_values() for estimated orientation or true_angle() for debugging')

    @property
    def velocity(self):
        """
        Disabled: Use estimated_linear_speed() for estimated speed or true_velocity() for debugging.

        Raises:
            DisabledFunctionError: This function is disabled to prevent direct access.
        """
        raise DisabledFunctionError('Function Disabled: Use estimated_linear_speed() or estimated_velocity() for estimated speed, or true_velocity() for debugging')

    @property
    def angular_velocity(self):
        """
        Disabled: Use estimated_angular_speed() for estimated speed or true_angular_velocity() for debugging.

        Raises:
            DisabledFunctionError: This function is disabled to prevent direct access.
        """
        raise DisabledFunctionError('Function Disabled: Use estimated_angular_speed() or estimated_velocity() for estimated speed, or true_angular_velocity() for debugging')

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
        Get the true orientation of the robot, in radians between -π and π.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the orientation estimated by the odometer sensor.
        But you can use it for debugging or logging.

        Returns:
            float: The true orientation in radians, normalized to [-π, π].
        """
        return normalize_angle(self.base._pm_body.angle)

    def true_velocity(self) -> np.ndarray:
        """
        Get the true velocity of the robot in 2D, in pixels per second.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the velocity estimated by the odometer sensor.
        But you can use it for debugging or logging.

        Returns:
            np.ndarray: The true velocity vector [vx, vy] in pixels per second.
        """
        return np.array(self.base._pm_body.velocity)

    def true_angular_velocity(self) -> float:
        """
        Get the true angular velocity of the robot, in radians per second.
        You must NOT use this value for your calculation in the control() function, instead you
        should use the velocity estimated by the odometer sensor.
        But you can use it for debugging or logging.

        Returns:
            float: The true angular velocity in radians per second.
        """
        return self.base._pm_body.angular_velocity


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
