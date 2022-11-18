from abc import ABC, abstractmethod
from typing import Type, Union

from spg.playground import Playground

from spg_overlay.entities.robot_abstract import RobotAbstract


class MapAbstract(ABC):
    """
    It is abstract class to construct every maps used in the directory maps
    """

    def __init__(self):
        self._size_area = None
        self._robot: Union[RobotAbstract, Type[None]] = None

    @abstractmethod
    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        pass

    @property
    def robot(self):
        return self._robot

    @property
    def size_area(self):
        return self._size_area

