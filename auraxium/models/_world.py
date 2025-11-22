"""Data classes for :mod:`auraxium.ps2._world`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'WorldData'
]


class WorldData(RESTPayload):
    """Data class for :class:`auraxium.ps2.World`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    world_id: int
    state: str
    name: LocaleData
    description: LocaleData | None = None
