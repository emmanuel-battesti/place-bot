from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk


if TYPE_CHECKING:
    from place_bot.simulation.gui_map.playground import Playground


def get_colliding_entities(playground: "Playground", arbiter: pymunk.Arbiter):
    """
    Retrieve the two old_entities involved in a collision from the arbiter.

    Args:
        playground (Playground): The playground instance.
        arbiter (pymunk.Arbiter): The collision arbiter.

    Returns:
        tuple: The two colliding old_entities.
    """
    shape_1, shape_2 = arbiter.shapes
    entity_1 = playground.get_entity_from_shape(shape_1)
    entity_2 = playground.get_entity_from_shape(shape_2)

    return entity_1, entity_2


