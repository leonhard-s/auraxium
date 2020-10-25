"""Zone class definition."""

from ..base import Named
from ..models import ZoneData


class Zone(Named, cache_size=20, cache_ttu=3600.0):
    """A continent or dynamic zone in the game world.

    Note that some dynamic zones are not resolvable via this object.
    Dynamic zones include Sanctuary, the Tutorial zones, and the outfit
    wars desolation maps.
    """

    collection = 'zone'
    data: ZoneData
    dataclass = ZoneData
    id_field = 'zone_id'

    # @property
    # def is_dynamic(self) -> bool:
    #     """Return whether the given zone is dynamic or not.

    #     Dynamic zones are spun up for individual players as required,
    #     such as the tutorial world space.
    #     """
    #     # TODO: Add dynamic zone detection
