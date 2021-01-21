"""Zone class definition."""

from .._base import Named
from ..models import ZoneData
from ..types import LocaleData

__all__ = [
    'Zone'
]

_STATIC_ZONES = [
    2,  # Indar
    4,  # Hossin
    6,  # Amerish
    8,  # Esamir
    96,  # VR Training (NC)
    97,  # VR Training (TR)
    98  # VR Training (VS)
]


class Zone(Named, cache_size=20, cache_ttu=3600.0):
    """A continent or dynamic zone in the game world.

    Note that some dynamic zones are not resolvable via this object.
    Dynamic zones include Sanctuary, the tutorial zones, and the outfit
    wars desolation maps.

    Attributes:
        zone_id: The unique ID of this zone.
        code: The internal code used to represent this zone.
        hex_size: The map size for this zone.
        description: The localised name of this zone.

    """

    collection = 'zone'
    data: ZoneData
    dataclass = ZoneData
    id_field = 'zone_id'

    # Type hints for data class fallback attributes
    zone_id: int
    code: str
    hex_size: int
    description: LocaleData

    @property
    def is_dynamic(self) -> bool:
        """Return whether the given zone is dynamic or not.

        Dynamic zones are spun up for individual players as needed,
        such as the tutorial or Sanctuary.
        """
        return self.id not in _STATIC_ZONES
