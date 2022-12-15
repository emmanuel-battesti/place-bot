import math
from abc import ABC

import numpy as np

from spg.agent.sensor.internal import InternalSensor
from place_bot.utils.utils import deg2rad, normalize_angle
from place_bot.utils.utils_noise import AutoregressiveModelNoise, GaussianNoise


class RobotOdometer(InternalSensor):
    """
      RobotOdometer sensor returns a numpy array containing:
      - dist_travel, the distance of the travel of the robot during one step
      - alpha, the relative angle of the current position seen from the previous reference frame of the robot
      - theta, the variation of orientation (or rotation) of the robot during the last step in the reference frame
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._noise = True

        self.std_dev_dist_travel = 0.2
        self.model_param_travel = 0.2
        self._noise_dist_travel_model = AutoregressiveModelNoise(model_param=self.model_param_travel,
                                                                 std_dev_noise=self.std_dev_dist_travel)

        self.std_dev_alpha = deg2rad(5.0)
        self.model_param_alpha = 0.2
        self._noise_alpha_model = AutoregressiveModelNoise(model_param=self.model_param_alpha,
                                                           std_dev_noise=self.std_dev_alpha)

        self.std_dev_theta = deg2rad(0.6)  # 0.6 deg = 0.0105 rad
        self.model_param_theta = 0.2
        self._noise_theta_model = AutoregressiveModelNoise(model_param=self.model_param_theta,
                                                           std_dev_noise=self.std_dev_theta)

        self._values = self._default_value
        self._delta = np.array([0.0, 0.0, 0.0])
        self.prev_angle = None
        self.prev_position = None

    def _compute_raw_sensor(self):
        # DIST_TRAVEL
        if self.prev_position is None:
            self.prev_position = self._anchor.position

        travel_vector = self._anchor.position - self.prev_position
        dist_travel = math.sqrt(travel_vector[0] ** 2 + travel_vector[1] ** 2)
        self._delta[0] = dist_travel

        # ALPHA
        if self.prev_angle is None:
            self.prev_angle = self._anchor.angle

        alpha = math.atan2(travel_vector[1], travel_vector[0]) - self.prev_angle
        self._delta[1] = normalize_angle(alpha)

        # THETA
        theta = self._anchor.angle - self.prev_angle
        self._delta[2] = normalize_angle(theta)

        # UPDATE
        self.prev_position = self._anchor.position
        self.prev_angle = self._anchor.angle

        if self._noise:
            self._apply_my_noise()

        self.integration()

    def integration(self):
        """
        Compute a new position of the robot by adding noisy displacement (delta) to the previous
        position. It updates self._values.
        """
        dist, alpha, theta = (0.0, 0.0, 0.0)
        if not self.is_disabled():
            dist, alpha, theta = tuple(self._delta)

        x, y, orient = tuple(self._values)
        new_x = x + dist * math.cos(alpha + orient)
        new_y = y + dist * math.sin(alpha + orient)
        new_orient = orient + theta

        new_orient = normalize_angle(new_orient)

        self._values = np.array([new_x, new_y, new_orient])

    def _apply_normalization(self):
        pass

    @property
    def _default_value(self) -> np.ndarray:
        return np.zeros(self.shape)

    def get_sensor_values(self):
        return self._values

    def draw(self):
        pass

    @property
    def shape(self) -> tuple:
        return 3,

    def _apply_noise(self):
        """
        Overload of an internal function of _apply_noise of the class InternalSensor
        As we have to do more computation (integration) after this function we cannot use it.
        In the function update() of sensor.pu in SPG, we call first _compute_raw_sensor() then _apply_noise. That all.
        We will use the function _apply_my_noise below instead.
        """
        pass

    def _apply_my_noise(self):
        """
        Overload of an internal function of _apply_noise of the class InternalSensor
        """
        noisy_dist_travel = self._noise_dist_travel_model.add_noise(self._delta[0])
        # print("travel: {:2f}, noisy_dist_travel: {:2f}".format(dist_travel, noisy_dist_travel))
        noisy_alpha = self._noise_alpha_model.add_noise(self._delta[1])
        noisy_theta = self._noise_theta_model.add_noise(self._delta[2])

        self._delta = np.array([noisy_dist_travel, noisy_alpha, noisy_theta])

    def is_disabled(self):
        return self._disabled
