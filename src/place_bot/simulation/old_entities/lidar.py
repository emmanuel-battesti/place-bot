import math
import numpy as np

from spg.agent.sensor import DistanceSensor

from place_bot.simulation.utils.utils_noise import GaussianNoise


# Helper function that computes the angles of the laser rays of the sensor in radians
def compute_ray_angles(fov_rad: float, nb_rays: int) -> np.ndarray:
    """
    The compute_ray_angles function calculates the angles of the laser rays of
    a sensor based on the field of view and the number of rays.

    Example Usage
        fov_rad = math.pi / 2
        nb_rays = 5
        ray_angles = compute_ray_angles(fov_rad, nb_rays)
        print(ray_angles)

        Output:
        [-0.78539816, -0.39269908, 0.0, 0.39269908, 0.78539816]

    Inputs
        fov_rad (float): The field of view in radians.
        nb_rays (int): The number of rays of the sensor.
    """

    if not isinstance(fov_rad, float) or fov_rad <= 0:
        raise ValueError("fov_rad must be a positive float.")

    if nb_rays == 1:
        ray_angles = [0.]
    else:
        ray_angles = np.linspace(-fov_rad / 2, fov_rad / 2, nb_rays)

    # 'ray_angles' is an array which contains the angles of the laser rays of
    # the sensor
    return np.array(ray_angles)


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
    It emulates a lidar.
    Lidar is an acronym of "light detection and ranging".
    It is a real sensor that measures distances with a laser in different directions.
    - fov (field of view): 360 degrees
    - resolution (number of rays): 181
    - max range (maximum range of the sensor): 300 pix
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

        # Set the sensor values to the default value (nan)
        self._values = self._default_value

        # Compute the ray angles
        self._ray_angles = compute_ray_angles(fov_rad=self.fov_rad(), nb_rays=self.resolution)

    def fov_rad(self):
        """Field of view in radians"""
        return self._fov

    def fov_deg(self):
        """ Field of view in degrees"""
        return self._fov * 180 / math.pi

    def get_sensor_values(self):
        """Get values of the lidar as a numpy array"""
        return self._values

    def get_ray_angles(self):
        """ Get ray angles in radians as a numpy array"""
        return self._ray_angles

    def is_disabled(self):
        """Returns a boolean indicating if the sensor is disabled."""
        return self._disabled

    def _apply_noise(self):
        """Applies noise to the lidar sensor values."""
        self._values = self._noise_model.add_noise(self._values)

    def draw(self):
        """Draws the lidar sensor rays."""
        # Check if hitpoints are defined
        hitpoints_ok = not isinstance(self._hitpoints, int)
        # If hitpoints are defined, call the base class draw method
        if hitpoints_ok:
            super().draw()

    # Property that returns the default value for the sensor values
    @property
    def _default_value(self):
        # Create an array of nan with the same shape as the Lidar's resolution
        null_sensor = np.empty(self.shape)
        null_sensor[:] = np.nan
        return null_sensor

    # Property that returns the shape of the sensor values
    @property
    def shape(self):
        return self._resolution,
