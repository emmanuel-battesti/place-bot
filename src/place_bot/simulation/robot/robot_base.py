import math

import arcade
import pymunk

from place_bot.resources import path_resources
from place_bot.simulation.robot.controller import CenteredContinuousController
from place_bot.simulation.robot.robot_part import RobotPart
from place_bot.simulation.utils.constants import LINEAR_SPEED_RATIO, ANGULAR_SPEED_RATIO
from place_bot.simulation.utils.definitions import LINEAR_FORCE, ANGULAR_VELOCITY, CollisionTypes


class RobotBase(RobotPart):
    """
    The RobotBase class represents a robot base in a simulation. It defines the
    behavior and properties of the robot, including its movement and control
     mechanisms.
    """

    def __init__(
            self,
            linear_ratio: float = LINEAR_SPEED_RATIO,
            angular_ratio: float = ANGULAR_SPEED_RATIO,
            **kwargs,
    ):
        """
        Initialize the RobotBase.

        Args:
            linear_ratio (float): Ratio for linear speed.
            angular_ratio (float): Ratio for angular speed.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            mass=50,
            filename=path_resources + "/robot.png",
            sprite_front_is_up=True,
            shape_approximation="hull",
            # radius=15,
            **kwargs,
        )

        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        # See: https://api.arcade.academy/en/latest/examples/pymunk_demo_top_down.html
        for pm_shape in self._pm_shapes:
            pm_shape.elasticity = 0.1
            pm_shape.friction = 0.7  # default value in arcade is 0.2

        self.forward_controller = CenteredContinuousController(name="forward")
        self.add_device(self.forward_controller)

        self.angular_vel_controller = (
            CenteredContinuousController(name="rotation"))
        self.add_device(self.angular_vel_controller)

        self.linear_ratio = LINEAR_FORCE * linear_ratio
        self.angular_ratio = ANGULAR_VELOCITY * angular_ratio

    def _apply_commands(self, **kwargs) -> None:
        """
        Apply the control commands to the robot's physical body.

        Args:
            **kwargs: Additional keyword arguments.
        """
        cmd_forward = self.forward_controller.command_value
        cmd_forward = max(min(cmd_forward, 1.0), -1.0)
        self._pm_body.apply_force_at_local_point(
            force=pymunk.Vec2d(cmd_forward, 0) * self.linear_ratio, point=(0, 0)
        )

        cmd_angular = self.angular_vel_controller.command_value
        self._pm_body.angular_velocity = cmd_angular * self.angular_ratio

    @property
    def _collision_type(self):
        """
        Returns the collision type for the robot base.
        """
        return CollisionTypes.ROBOT
