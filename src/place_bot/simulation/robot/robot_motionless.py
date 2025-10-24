from place_bot.simulation.robot.controller import CommandsDict
from place_bot.simulation.robot.robot_abstract import RobotAbstract


class RobotMotionless(RobotAbstract):
    """
    A robot that does not move. Used for testing or as a static agent.
    """

    def __init__(self, **kwargs):
        """
        Initialize a motionless robot.

        Args:
            **kwargs: Additional keyword arguments (lidar_params, odometer_params).
        """
        super().__init__(**kwargs)

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
