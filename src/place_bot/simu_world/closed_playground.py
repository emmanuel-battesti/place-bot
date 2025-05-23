import platform
from typing import Tuple

from spg.playground import Playground

from place_bot.entities.normal_wall import NormalWall


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

    def __init__(self, size: Tuple[int, int], use_shaders: bool = True):
        background = (220, 220, 220)

        if platform.system() == "Darwin":
            use_shaders = False

        super().__init__(size=size,
                         seed=None,
                         background=background,
                         use_shaders=use_shaders)

        assert isinstance(self._width, int)
        assert isinstance(self._height, int)

        border_thickness: int = 6
        self._walls_creation(border_thickness)

        # print(f"Version OpenGL : {self._window.ctx.gl_version}")

    def _walls_creation(self, border_thickness):
        h = self._height / 2
        w = self._width / 2
        o = border_thickness / 2
        pts = [
            [(-w + o, -h), (-w + o, h), ],
            [(-w, h - o), (w, h - o)],
            [(w - o, h), (w - o, -h)],
            [(w, -h + o), (-w, -h + o), ],
        ]
        for begin_pt, end_pt in pts:
            wall = NormalWall(pos_start=begin_pt, pos_end=end_pt,
                              wall_thickness=border_thickness)
            self.add(wall, wall.wall_coordinates)
