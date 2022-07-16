"""Zone class definition."""

from ..base import Named
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
    98,  # VR Training (VS)
    344,  # Oshur
]


class Zone(Named, cache_size=20, cache_ttu=3600.0):
    """A continent or dynamic zone in the game world.

    Note that some dynamic zones are not resolvable via this object.
    Dynamic zones include Sanctuary, the tutorial zones, and the outfit
    wars desolation maps.

    .. attribute:: id
       :type: int

       The unique ID of this zone. In the API payload, this field
       is called ``zone_id``.

    .. attribute:: code
       :type: str

       The internal code used to represent this zone.

    .. attribute:: hex_size
       :type: int

       The map size for this zone.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The localised name of this zone.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the zone.
    """

    collection = 'zone'
    data: ZoneData
    id_field = 'zone_id'
    _model = ZoneData

    # Type hints for data class fallback attributes
    id: int
    code: str
    hex_size: int
    description: LocaleData
    name: LocaleData

    @property
    def is_dynamic(self) -> bool:
        """Return whether the given zone is dynamic or not.

        Dynamic zones are spun up for individual players as needed,
        such as the tutorial or Sanctuary.
        """
        return self.id not in _STATIC_ZONES
