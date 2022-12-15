import math
from abc import ABC

import numpy as np

from spg.agent.sensor.internal import InternalSensor
from place_bot.utils.utils import deg2rad, rad2deg, normalize_angle


class OdometerV2(InternalSensor):
    """
      Odometer sensor returns a numpy array containing:
      - dist_travel, the distance of the travel of the robot during one step
      - alpha, the relative angle of the current position seen from the previous reference frame of the robot
      - theta, the variation of orientation (or rotation) of the robot during the last step in the reference frame

      For the noise model, see:
      - https://blog.lxsang.me/post/id/16
      - https://www.mrpt.org/tutorials/programming/odometry-and-motion-models/probabilistic_motion_models/
      - https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf  page 113
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._noise = True

        self.param1 = 0.001  # degree/degree, influence of rotation to rotation
        self.param2 = 0.0  # degree/meter, influence of translation to rotation
        self.param3 = 0.0  # 0.2  # meter/meter, influence of translation to translation
        self.param4 = 0.0  # meter/degree, influence of rotation to translation

        self._values = self._default_value
        self._rot1 = 0
        self._trans = 0
        self._rot2 = 0
        self.prev_angle = None
        self.prev_position = None

    def _compute_raw_sensor(self):

        if self.prev_position is None:
            self.prev_position = self._anchor.position

        travel_vector = self._anchor.position - self.prev_position

        has_translated = True
        if abs(travel_vector[0]) < 1e-3 and abs(travel_vector[1]) < 1e-3:
            has_translated = False

        if self.prev_angle is None:
            self.prev_angle = self._anchor.angle

        has_turned = True
        if abs(self._anchor.angle - self.prev_angle) < 1e-3:
            has_turned = False

        # ROT1
        if has_translated and has_turned:
            rot1 = math.atan2(travel_vector[1], travel_vector[0]) - self.prev_angle
            self._rot1 = normalize_angle(rot1)
        else:
            self._rot1 = 0

        # TRANS
        if has_translated:
            self._trans = math.sqrt(travel_vector[0] ** 2 + travel_vector[1] ** 2)
        else:
            self._trans = 0

        # ROT2
        if has_turned:
            rot2 = self._anchor.angle - self.prev_angle - self._rot1
            self._rot2 = normalize_angle(rot2)
        else:
            self._rot2 = 0

        print(rad2deg(self._rot1), self._trans, rad2deg(self._rot2))

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
        x, y, orient = tuple(self._values)
        new_x = x + self._trans * math.cos(orient + self._rot1)
        new_y = y + self._trans * math.sin(orient + self._rot1)
        new_orient = orient + self._rot1 + self._rot2

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
        As we have to do more computation (integration) after this function, we cannot use it.
        In the function update() of sensor.pu in SPG, we call first _compute_raw_sensor() then _apply_noise. That all.
        We will use the function _apply_my_noise below instead.
        """
        pass

    def _apply_my_noise(self):
        """
        Overload of an internal function of _apply_noise of the class InternalSensor
        """
        sd_rot1 = self.param1 * rad2deg(abs(self._rot1)) + self.param2 * self._trans
        sd_trans = self.param3 * self._trans + self.param4 * rad2deg(abs(self._rot1) + abs(self._rot2))
        sd_rot2 = self.param1 * rad2deg(abs(self._rot2)) + self.param2 * self._trans

        self._rot1 += np.random.normal(0, sd_rot1 * sd_rot1)
        self._trans += np.random.normal(0, sd_trans * sd_trans)
        self._rot2 += np.random.normal(0, sd_rot2 * sd_rot2)

    def is_disabled(self):
        return self._disabled
