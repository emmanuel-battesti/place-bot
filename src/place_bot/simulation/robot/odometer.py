import math
from typing import Optional

import numpy as np

from place_bot.simulation.robot.sensor import Sensor
from place_bot.simulation.utils.utils import rad2deg, normalize_angle


class OdometerParams:
    """
    Class containing parameters for the Odometer sensor

    Parameters:
    - param1 (float): Influence of translation on translation
    - param2 (float): Influence of rotation on translation
    - param3 (float): Influence of translation on rotation
    - param4 (float): Influence of rotation on rotation
    """
    param1 = 0.3  # 0.3  # meter/meter, influence of translation to translation
    param2 = 0.1  # 0.1  # meter/degree, influence of rotation to translation
    param3 = 0.04  # 0.04 # degree/meter, influence of translation to rotation
    param4 = 0.01  # 0.01 # degree/degree, influence of rotation to rotation


class Odometer(Sensor):
    """
    Odometer sensor that estimates robot position through dead reckoning.

    The sensor computes displacement at each timestep using three values:
    - dist_travel: Distance traveled during the last timestep
    - alpha: Relative angle of the current position from the previous robot frame
    - theta: Orientation change (rotation) during the last timestep

    These raw values are then INTEGRATED over time to estimate the robot's
    cumulative position and orientation since initialization.

    The get_sensor_values() method returns the INTEGRATED position estimate:
    - x: Estimated x position (in pixels) from starting point
    - y: Estimated y position (in pixels) from starting point
    - orientation: Estimated orientation (in radians, -π to π) from starting orientation

    Gaussian noise is added to the raw displacement values before integration
    to simulate real odometry sensor errors. The noise model is based on:
    - https://blog.lxsang.me/post/id/16
    - https://www.mrpt.org/tutorials/programming/odometry-and-motion-models/probabilistic_motion_models/
    - https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf (page 113)

    Note: I could not use directly the model given in the first link, because my robot slides a bit sideways.
    This causes calculation problems. If the robot moves sideways, it will be calculated that the robot has done
    a 90° degree rotation, moved straight and then another 90° in the other direction. This distorts the
    calculations of the noise...
    """

    def __init__(self, odometer_params: OdometerParams = OdometerParams(), **kwargs):
        """
        Initialize the Odometer sensor instance.

        Parameters:
        - odometer_params: an OdometerParams instance containing parameters for the sensor
        - kwargs: other keyword arguments
        """
        super().__init__(**kwargs)
        self._noise = True

        self.param1 = odometer_params.param1
        self.param2 = odometer_params.param2
        self.param3 = odometer_params.param3
        self.param4 = odometer_params.param4

        self._values = self._default_value
        self._dist = 0
        self._alpha = 0
        self._theta = 0
        self.prev_angle = None
        self.prev_position = None

    def _compute_raw_sensor(self) -> None:
        """
        Compute the raw displacement values and integrate them to update position estimate.

        This method:
        1. Computes raw displacement (dist_travel, alpha, theta) from robot movement
        2. Applies Gaussian noise to simulate real sensor errors
        3. Integrates the noisy displacement to update the estimated position

        Raw displacement values computed:
        - _dist: Distance traveled since last timestep (in pixels)
        - _alpha: Relative angle of movement in previous robot frame (in radians)
        - _theta: Change in orientation since last timestep (in radians)

        These raw values are NOT returned by get_sensor_values(). They are used
        internally for integration to compute the cumulative position estimate.
        """
        # DIST_TRAVEL
        if self.prev_position is None:
            self.prev_position = self._anchor.position

        travel_vector = self._anchor.position - self.prev_position
        self._dist = math.sqrt(travel_vector[0] ** 2 + travel_vector[1] ** 2)

        has_translated = True
        if abs(self._dist) < 1e-5:
            has_translated = False

        # ALPHA
        if self.prev_angle is None:
            self.prev_angle = self._anchor.angle

        if has_translated:
            alpha = math.atan2(travel_vector[1], travel_vector[0]) - self.prev_angle
        else:
            alpha = 0
        self._alpha = normalize_angle(alpha)

        # THETA
        theta = self._anchor.angle - self.prev_angle
        self._theta = normalize_angle(theta)

        # UPDATE
        self.prev_position = self._anchor.position
        self.prev_angle = self._anchor.angle

        if self._noise:
            self._apply_my_noise()

        self.integration()

    def integration(self) -> None:
        """
        Integrate noisy displacement to update the estimated position.

        This method computes the new estimated position (x, y, orientation) by adding
        the noisy displacement (dist, alpha, theta) to the previous estimated position.
        This is the core of dead reckoning: accumulating incremental movements over time.

        The integration uses the following formulas:
        - new_x = x + dist * cos(alpha + orient)
        - new_y = y + dist * sin(alpha + orient)
        - new_orient = orient + theta

        This updates self._values with the new integrated position.
        """
        x, y, orient = tuple(self._values)
        new_x = x + self._dist * math.cos(self._alpha + orient)
        new_y = y + self._dist * math.sin(self._alpha + orient)
        new_orient = orient + self._theta

        new_orient = normalize_angle(new_orient)

        self._values = np.array([new_x, new_y, new_orient])

    def _apply_normalization(self) -> None:
        """
        No normalization applied for odometer.
        """
        pass

    @property
    def _default_value(self) -> np.ndarray:
        """
        Returns the default value for the sensor.
        """
        return np.zeros(self.shape)

    def get_sensor_values(self) -> Optional[np.ndarray]:
        """
        Get the integrated odometer position estimate.

        This method returns the estimated position of the robot computed by
        integrating noisy displacement measurements over time since initialization.

        Returns:
            Optional[np.ndarray]: Array containing [x, y, orientation] where:
                - x (float): Estimated x position in pixels from starting point
                - y (float): Estimated y position in pixels from starting point
                - orientation (float): Estimated orientation in radians (-π to π) from starting orientation
                Returns None if the sensor is disabled.

        Note:
            This is NOT the raw displacement (dist_travel, alpha, theta) but the
            accumulated/integrated position estimate. The raw values are used
            internally but not exposed.
        """
        if not self._disabled:
            return self._values
        else:
            return None

    def draw(self) -> None:
        """
        Draws the odometer sensor (no-op).
        """
        pass

    @property
    def shape(self) -> tuple:
        """
        Returns the shape of the sensor output.
        """
        return 3,

    def _apply_noise(self) -> None:
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
        sd_trans = self.param1 * self._dist + self.param2 * rad2deg(abs(self._theta))
        sd_rot = self.param3 * self._dist + self.param4 * rad2deg(abs(self._theta))

        noisy_alpha = self._alpha + np.random.normal(0, sd_rot * sd_rot)
        noisy_dist_travel = self._dist + np.random.normal(0, sd_trans * sd_trans)
        noisy_theta = self._theta + np.random.normal(0, sd_rot * sd_rot)

        self._dist = noisy_dist_travel
        self._alpha = noisy_alpha
        self._theta = noisy_theta

    def is_disabled(self) -> bool:
        """
        Returns whether the sensor is disabled.

        Returns:
            bool: True if disabled, False otherwise.
        """
        return self._disabled

    def get_last_displacement(self) -> tuple[float, float, float]:
        """
        Get the last raw displacement values before integration.

        This method is provided for debugging and analysis purposes.
        These are the noisy raw displacement values from the last timestep,
        NOT the integrated position.

        Returns:
            tuple[float, float, float]: Tuple containing:
                - dist (float): Distance traveled during last timestep (in pixels)
                - alpha (float): Relative angle in previous robot frame (in radians)
                - theta (float): Orientation change during last timestep (in radians)

        Note:
            These values include the noise model applied to simulate real sensors.
            Use this for debugging or to understand the raw sensor data before integration.
        """
        return (self._dist, self._alpha, self._theta)

