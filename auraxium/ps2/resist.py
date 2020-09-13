"""Resistance mapping class definitions."""

from ..base import Cached
from ..census import Query
from ..models import ResistInfoData, ResistTypeData
from ..proxy import InstanceProxy
from ..types import CensusData


class ResistType(Cached, cache_size=100, cache_ttu=60.0):
    """A type of resistance a profile may hold.

    This is used to implement weapon types like "Melee", "Small Arms"
    or "Heavy Machine Gun".
    """

    collection = 'resist_type'
    data: ResistTypeData
    id_field = 'resist_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ResistTypeData:
        return ResistTypeData.from_census(data)


class ResistInfo(Cached, cache_size=100, cache_ttu=60.0):
    """Specifies the resistance values for a given profile and type."""

    collection = 'resist_info'
    data: ResistInfoData
    id_field = 'resist_info_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ResistInfoData:
        return ResistInfoData.from_census(data)

    def type(self) -> InstanceProxy[ResistType]:
        """Return the resist type for this entry.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            ResistType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ResistType.id_field, value=self.data.resist_type_id)
        return InstanceProxy(ResistType, query, self._client)
