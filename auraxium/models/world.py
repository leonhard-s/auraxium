"""Data classes for :mod:`auraxium.ps2.world`."""

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'WorldData'
]


class WorldData(Ps2Data):
    """Data class for :class:`auraxium.ps2.world.World`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        world_id: The unique ID of the world.
        state: The current state (i.e. online status) of the world.
        name: The localised name of the world.
        description: A description of the world's server region.

    """

    world_id: int
    state: str
    name: LocaleData
    description: LocaleData
