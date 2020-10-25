"""Data classes for :mod:`auraxium.ps2.zone`."""

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'ZoneData'
]


class ZoneData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone.Zone`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        zone_id: The unique ID of this zone.
        code: The internal code used to represent this zone.
        hex_size: The map size for this zone.
        name: The localised name of this zone.
        description: The localised name of this zone.

    """

    zone_id: int
    code: str
    hex_size: int
    name: LocaleData
    description: LocaleData
