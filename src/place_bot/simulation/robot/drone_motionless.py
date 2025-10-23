from typing import Optional

from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.utils.misc_data import MiscData


class RobotMotionless(RobotAbstract):
    """
    A robot that does not move. Used for testing or as a static agent.
    """

    def __init__(
        self,
        identifier: Optional[int] = None,
        misc_data: Optional[MiscData] = None,
        **kwargs,
    ):
        """
        Initialize a motionless robot.

        Args:
            identifier (Optional[int]): Unique identifier for the robot.
            misc_data (Optional[MiscData]): Miscellaneous data.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            identifier=identifier,
            misc_data=misc_data,
            display_lidar_graph=False,
            **kwargs
        )

    def define_message_for_all(self) -> None:
        """
        Define the message to be sent to all nearby robots.
        This robot does not send any messages.
        """
        pass

    def control(self) -> CommandsDict:
        """
        The robot will not move.

        Returns:
            CommandsDict: All commands set to zero.
        """
        command_motionless: CommandsDict = {
            "forward": 0.0,
            "lateral": 0.0,
            "rotation": 0.0,
            "grasper": 0
        }
        return command_motionless
