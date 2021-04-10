"""Resistance mapping class definitions."""

from typing import Optional
from ..base import Cached
from ..census import Query
from ..models import ResistInfoData, ResistTypeData
from .._proxy import InstanceProxy

__all__ = [
    'ResistInfo',
    'ResistType'
]


class ResistType(Cached, cache_size=100, cache_ttu=60.0):
    """A type of resistance a profile may hold.

    This is used to implement weapon types like "Melee", "Small Arms"
    or "Heavy Machine Gun".

    Attributes:
        id: The unique ID of this resist type.
        description: A description of what this resist type is used
            for.

    """

    collection = 'resist_type'
    data: ResistTypeData
    id_field = 'resist_type_id'
    _model = ResistTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str


class ResistInfo(Cached, cache_size=100, cache_ttu=60.0):
    """Specifies the resistance values for a given profile and type.

    Attributes:
        id: The ID of this resist info entry.
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
    id_field = 'resist_info_id'
    _model = ResistInfoData

    # Type hints for data class fallback attributes
    id: int
    resist_type_id: int
    resist_percent: Optional[int]
    resist_amount: Optional[int]
    multiplier_when_headshot: Optional[float]
    description: str

    def type(self) -> InstanceProxy[ResistType]:
        """Return the resist type for this entry.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            ResistType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ResistType.id_field, value=self.data.resist_type_id)
        return InstanceProxy(ResistType, query, self._client)
