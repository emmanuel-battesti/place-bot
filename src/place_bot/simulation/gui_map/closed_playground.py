import platform
from typing import Tuple

from place_bot.simulation.robot.agent import Agent
from place_bot.simulation.elements.embodied import EmbodiedEntity
from place_bot.simulation.elements.normal_wall import NormalWall
from place_bot.simulation.gui_map.playground import Playground


class ClosedPlayground(Playground):
    """
    The ClosedPlayground class is a subclass of the Playground class. It
    represents a closed playground with walls surrounding it. The class
    initializes the playground with a specified size and sets the background
    color. It also determines whether to use shaders based on the platform.
    The class defines the shape of the walls and adds them to the playground.

    Example Usage
        playground = ClosedPlayground((800, 600))

        In this example, a ClosedPlayground object is created with a size of
        800x600 pixels. The playground will have walls surrounding it and a
        default background color. The playground can then be used for various
        purposes, such as simulating physics or rendering graphics.

    Fields
        _width: The width of the playground.
        _height: The height of the playground.
    """

    def __init__(self, size: Tuple[int, int], use_shaders: bool = True, border_thickness: int = 6):
        """
        Initialize the ClosedPlayground.

        Args:
            size (Tuple[int, int]): Size of the playground (width, height).
            border_thickness (int): Thickness of the border walls.
        """
        background = (220, 220, 220)

        if platform.system() == "Darwin":
            use_shaders = False

        super().__init__(size=size,
                         seed=None,
                         background=background,
                         use_shaders=use_shaders)

        assert isinstance(self.size[0], int)
        assert isinstance(self.size[1], int)

        self._walls_creation(border_thickness)

        # print(f"Version OpenGL : {self._window.ctx.gl_version}")

    def _walls_creation(self, border_thickness: int) -> None:
        """
        Create the border walls for the playground.

        Args:
            border_thickness (int): Thickness of the border walls.
        """
        width, height = self.size
        h = height / 2
        w = width / 2
        o = border_thickness / 2
        pts = [
            [(-w + o, -h), (-w + o, h)],
            [(-w, h - o), (w, h - o)],
            [(w - o, h), (w - o, -h)],
            [(w, -h + o), (-w, -h + o)],
        ]
        for begin_pt, end_pt in pts:
            wall = NormalWall(pos_start=begin_pt, pos_end=end_pt,
                              wall_thickness=border_thickness)
            self.add(wall, wall.wall_coordinates)

    def get_closest_robot(self, entity: EmbodiedEntity) -> Agent:
        """
        Get the closest robot agent to a given entity.

        Args:
            entity (EmbodiedEntity): The entity to compare distances to.

        Returns:
            Agent: The closest agent.
        """
        return min(self.agents, key=lambda a: entity.position.get_dist_sqrd(a.true_position()))
