"""Object representations for the PlanetSide 2 API.

This is a higher-level abstraction of the data accessible through the
census. Note that the object attributes and hierarchy of this object
model will not match up to the Census API perfectly.
"""

from .character import Character
from .faction import Faction
from .item import Item
from .weapon import Weapon

__all__ = ['Character', 'Faction', 'Item', 'Weapon']
