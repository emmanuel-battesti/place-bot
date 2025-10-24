import math
from typing import Optional

import numpy as np

from place_bot.simulation.ray_sensors.distance_sensor import DistanceSensor, compute_ray_angles
from place_bot.simulation.utils.utils_noise import GaussianNoise


# Class that holds the parameters of a Lidar instance
class LidarParams:
    # Field of view (FOV) in degrees
    fov = 360
    # Resolution (number of rays)
    resolution = 361
    # Maximum range (maximum distance that the sensor can measure) in pixels
    max_range = 600
    # Flag that enables/disables noise
    noise_enable = True
    # Standard deviation of the noise to add to sensor readings
    std_dev_noise = 2.5


# Class that emulates a Lidar sensor
class Lidar(DistanceSensor):
    """
    The Lidar class is a subclass of the DistanceSensor class and
    represents a lidar sensor for a robot.
    It emulates a real lidar sensor ("light detection and ranging") that
    measures distances using a laser in different directions. The class provides
     methods to calculate the field of view in radians and degrees, get the
     sensor values, check if the sensor is disabled, apply noise to the sensor
     values, and draw the lidar sensor.

    It is a real sensor that measures distances with a laser in different
    directions.
    - fov (field of view): 360 degrees
    - resolution (number of rays): 361
    - max range (maximum range of the sensor): 600 pix
    """

    def __init__(self, lidar_params: LidarParams = LidarParams(), invisible_elements=None, **kwargs):
        # Initialize the base class
        super().__init__(normalize=False,
                         fov=lidar_params.fov,
                         resolution=lidar_params.resolution,
                         max_range=lidar_params.max_range,
                         invisible_elements=invisible_elements,
                         **kwargs)

        # Set the noise flag and standard deviation
        self._noise = lidar_params.noise_enable
        self._std_dev_noise = lidar_params.std_dev_noise
        # Create a noise model based on Gaussian noise
        self._noise_model = GaussianNoise(mean_noise=0, std_dev_noise=self._std_dev_noise)

        # '_ray_angles' is an array which contains the angles of the laser rays
        # of the sensor
        self._ray_angles = compute_ray_angles(fov_rad=self.fov_rad(), nb_rays=self.resolution)

        # Set the sensor values to the default value (nan)
        self._values = self._default_value

    def get_ray_angles(self) -> np.ndarray:
        """
        Get the angles of the laser rays of the sensor.

        Returns:
            np.ndarray: Array containing the angles of the laser rays in radians.
        """
        return self._ray_angles

    def fov_rad(self) -> float:
        """
        Returns the field of view in radians.
        """
        return self._fov

    def fov_deg(self) -> float:
        """
        Returns the field of view in degrees.
        """
        return math.degrees(self._fov)

    def get_sensor_values(self) -> Optional[np.ndarray]:
        """
        Get values of the lidar as a numpy array.

        Returns:
            np.ndarray or None: Sensor values or None if disabled.
        """
        if not self._disabled:
            return self._values
        else:
            return None

    def is_disabled(self) -> bool:
        """
        Returns a boolean indicating if the sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self._disabled

    def _apply_noise(self) -> None:
        """
        Applies noise to the sensor values.
        """
        self._values = self._noise_model.add_noise(self._values)

    def draw(self) -> None:
        """
        Draws the rays of lidar sensor.
        """
        if self._hitpoints is not None:
            super().draw()

    @property
    def _default_value(self) -> np.ndarray:
        """
        Returns the default value for the sensor.
        """
        # Create an array of nan with the same shape as the Lidar's resolution
        null_sensor = np.empty(self.shape)
        null_sensor[:] = np.nan
        return null_sensor

    @property
    def shape(self) -> tuple:
        """
        Returns the shape of the sensor output.
        """
        return self._resolution,
