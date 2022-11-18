import math
from collections import namedtuple

import numpy as np
from enum import Enum, auto

from spg.agent import Agent
from spg.agent.sensor import DistanceSensor
from spg.element import ColorWall
from spg.playground import Playground

from spg_overlay.entities.normal_wall import NormalWall, NormalBox
from spg_overlay.utils.utils_noise import GaussianNoise


def compute_ray_angles(fov_rad: float, nb_rays: int) -> np.ndarray:
    a = fov_rad / (nb_rays - 1)
    b = fov_rad / 2
    if nb_rays == 1:
        ray_angles = [0.]
    else:
        ray_angles = [n * a - b for n in range(nb_rays)]

    # 'ray_angles' is an array which contains the angles of the laser rays of the sensor
    return np.array(ray_angles)


class RobotDistanceSensor(DistanceSensor):
    def __init__(self, noise=True, **kwargs):
        super().__init__(**kwargs)

        self._noise = noise
        self._std_dev_noise = 2.5
        self._noise_model = GaussianNoise(mean_noise=0, std_dev_noise=self._std_dev_noise)

        self._values = self._default_value

        # 'ray_angles' is an array which contains the angles of the laser rays of the sensor
        self.ray_angles = compute_ray_angles(fov_rad=self.fov_rad(), nb_rays=self.resolution)

    def fov_rad(self):
        """Field of view in radians"""
        return self._fov

    def fov_deg(self):
        """ Field of view in degrees"""
        return self._fov * 180 / math.pi

    def get_sensor_values(self):
        """Get values of the lidar as a numpy array"""
        return self._values

    def is_disabled(self):
        return self._disabled

    def _apply_noise(self):
        self._values = self._noise_model.add_noise(self._values)

    def draw(self):
        hitpoints_ok = not isinstance(self._hitpoints, int)
        if hitpoints_ok:
            super().draw()

    @property
    def _default_value(self):
        null_sensor = np.empty(self.shape)
        null_sensor[:] = np.nan
        return null_sensor

    @property
    def shape(self):
        return self._resolution,


class RobotLidar(RobotDistanceSensor):
    """
    It emulates a lidar.
    Lidar is an acronym of "light detection and ranging".
    It is a real sensor that measures distances with a laser in different directions.
    - fov (field of view): 360 degrees
    - resolution (number of rays): 181
    - max range (maximum range of the sensor): 300 pix
    """

    def __init__(self, noise=True, invisible_elements=None, **kwargs):
        super().__init__(normalize=False,
                         fov=360,
                         resolution=181,
                         max_range=300,
                         invisible_elements=invisible_elements,
                         noise=noise,
                         **kwargs)
