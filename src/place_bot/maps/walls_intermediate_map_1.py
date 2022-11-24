"""
This file was generated by the tool 'image_to_map.py' in the directory tools.
This tool permits to create this kind of file by providing it an image of the map we want to create.
"""

from place_bot.spg_overlay.entities.normal_wall import NormalWall


# Dimension of the map : (800, 500)
# Dimension factor : 1.0
def add_boxes(_):
    pass


def add_walls(playground):

    # vertical wall 2
    wall = NormalWall(pos_start=(11.0, 250.0),
                      pos_end=(11.0, -93.0))
    playground.add(wall, wall.wall_coordinates)

    # vertical wall 3
    wall = NormalWall(pos_start=(13.0, 250.0),
                      pos_end=(13.0, -93.0))
    playground.add(wall, wall.wall_coordinates)

    # vertical wall 4
    wall = NormalWall(pos_start=(-225.0, 89.0),
                      pos_end=(-225.0, -250.0))
    playground.add(wall, wall.wall_coordinates)

    # vertical wall 5
    wall = NormalWall(pos_start=(-227.0, 89.0),
                      pos_end=(-227.0, -250.0))
    playground.add(wall, wall.wall_coordinates)

