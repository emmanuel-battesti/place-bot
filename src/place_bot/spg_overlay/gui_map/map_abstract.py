from abc import ABC, abstractmethod
from typing import List, Type

from spg.playground import Playground

from spg_overlay.entities.robot_abstract import RobotAbstract


class MapAbstract(ABC):
    """
    It is abstract class to construct every maps used in the directory maps
    """

    def __init__(self):
        self._size_area = None
        self._robot: Union[RobotAbstract, Type[None]] = None
        # '_time_step_limit' is the number of time steps after which the session will end.
        self._time_step_limit = None
        # 'real_time_limit' is the elapsed time (in seconds) after which the session will end.
        self._real_time_limit = None  # In seconds

    @abstractmethod
    def construct_playground(self, robot_type: Type[RobotAbstract]) -> Playground:
        pass

    @property
    def robot(self):
        return self._robot

    @property
    def time_step_limit(self):
        return self._time_step_limit

    @property
    def real_time_limit(self):
        return self._real_time_limit

    @property
    def size_area(self):
        return self._size_area

