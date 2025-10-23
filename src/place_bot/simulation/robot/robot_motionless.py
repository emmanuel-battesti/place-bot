from typing import Optional

from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_abstract import RobotAbstract


class RobotMotionless(RobotAbstract):
    """
    A robot that does not move. Used for testing or as a static agent.
    """

    def __init__(
        self,
        identifier: Optional[int] = None,
        **kwargs,
    ):
        """
        Initialize a motionless robot.

        Args:
            identifier (Optional[int]): Unique identifier for the robot.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(
            identifier=identifier,
            display_lidar_graph=False,
            **kwargs
        )

    def define_message_for_all(self) -> None:
        """
        Define the message to be sent to all nearby robot.
        This robot does not send any messages.
        """
        pass

    def control(self) -> CommandsDict:
        """
        The Robot will not move.

        Returns:
            CommandsDict: All commands set to zero.
        """
        command_motionless: CommandsDict = {
            "forward": 0.0,
            "rotation": 0.0,
        }
        return command_motionless
