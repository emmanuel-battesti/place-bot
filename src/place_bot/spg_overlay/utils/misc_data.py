from typing import Tuple


class MiscData:
    """
    This class should be used to contain miscellaneous data for the robot
    """

    def __init__(self,
                 size_area: Tuple[float, float] = None,
                 number_robots: int = None
                 ):
        self.size_area = size_area
        self.number_robots = number_robots
