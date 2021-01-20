"""Resistance mapping class definitions."""

from typing import Optional
from ..base import Cached
from ..census import Query
from ..models import ResistInfoData, ResistTypeData
from ..proxy import InstanceProxy


class ResistType(Cached, cache_size=100, cache_ttu=60.0):
    """A type of resistance a profile may hold.

    This is used to implement weapon types like "Melee", "Small Arms"
    or "Heavy Machine Gun".

    Attributes:
        resist_type_id: The unique ID of this resist type.
        description: A description of what this resist type is used
            for.

    """

    collection = 'resist_type'
    data: ResistTypeData
    dataclass = ResistTypeData
    id_field = 'resist_type_id'

    # Type hints for data class fallback attributes
    resist_type_id: int
    description: str


class ResistInfo(Cached, cache_size=100, cache_ttu=60.0):
    """Specifies the resistance values for a given profile and type.

    Attributes:
        resist_info: The ID of this resist info entry.
        resist_type_id: The ID of the :class:`ResistType` for this
            entry.
        resist_percent: The damage reduction in percent.
        resist_amount: A flat amount of damage to absorb.
        multiplier_when_headshot: A headshot multiplier override to
            apply.
        description: A description of this resist info entry.

    """

    collection = 'resist_info'
    data: ResistInfoData
    dataclass = ResistInfoData
    id_field = 'resist_info_id'

    # Type hints for data class fallback attributes
    resist_info_id: int
    resist_type_id: int
    resist_percent: Optional[int]
    resist_amount: Optional[int]
    multiplier_when_headshot: Optional[float]
    description: str

    def type(self) -> InstanceProxy[ResistType]:
        """Return the resist type for this entry.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            ResistType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ResistType.id_field, value=self.data.resist_type_id)
        return InstanceProxy(ResistType, query, self._client)
