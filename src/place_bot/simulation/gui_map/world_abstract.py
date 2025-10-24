from abc import ABC
from typing import Type, Union, Optional

from place_bot.simulation.robot.robot_abstract import RobotAbstract
from place_bot.simulation.gui_map.playground import Playground


class WorldAbstract(ABC):
    """
    The WorldAbstract class is an abstract class that serves as a blueprint for
    constructing different types of maps used in the directory "maps".
    """

    def __init__(self, robot: Union[RobotAbstract, None]):
        """
        Initialize the WorldAbstract.

        Args:
            robot (RobotAbstract): The robot instance to use.
        """
        self._playground: Optional[Playground] = None
        self._robot = robot
        self._size_area = None


    @property
    def playground(self) -> Union[Playground, Type[None]]:
        """
        Returns the playground instance.

        Returns:
            Playground or None: The playground.
        """
        return self._playground

    @property
    def robot(self) -> RobotAbstract:
        """
        Returns the robot in the world.

        Returns:
            RobotAbstract: The robot instance.
        """
        return self._robot

    @property
    def size_area(self):
        """
        Returns the size of the area.

        Returns:
            Any: The size of the area.
        """
        return self._size_area


