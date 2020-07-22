"""Resistance mapping class definitions."""

import dataclasses
from typing import Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..utils import optional
from ..types import CensusData


@dataclasses.dataclass(frozen=True)
class ResistTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_type_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ResistTypeData':
        return cls(
            int(data['resist_type_id']),
            str(data['description']))


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


@dataclasses.dataclass(frozen=True)
class ResistInfoData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    resist_info_id: int
    resist_type_id: int
    resist_percent: Optional[int]
    resist_amount: Optional[int]
    multiplier_when_headshot: Optional[float]
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ResistInfoData':
        return cls(
            int(data['resist_info_id']),
            int(data['resist_type_id']),
            optional(data, 'resist_percent', int),
            optional(data, 'resist_amount', int),
            optional(data, 'multiplier_when_headshot', float),
            str(data['description']))


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
