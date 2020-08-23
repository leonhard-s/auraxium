"""Ability and ability type class definitions."""

import dataclasses
from typing import List, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..types import CensusData
from ..utils import optional

from .ability import Ability


@dataclasses.dataclass(frozen=True)
class ZoneEffectTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone_effect.ZoneEffectType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes: 
        zone_effect_type_id: The unique ID of this zone effect type.
        description: A description of what this zone effect type is
            used for.
        param*: Descriptions of what the corresponding parameter is
            used for in zone effects of this type.

    """

    zone_effect_type_id: int
    description: str
    param1: str
    param2: str
    param3: str
    param4: str
    param5: str
    param6: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ZoneEffectTypeData':
        params: List[str] = [str(data[f'param{i+1}']) for i in range(6)]
        return cls(
            int(data['zone_effect_type_id']),
            str(data['description']),
            *params)


class ZoneEffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of zone effect.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'zone_effect_type'
    data: ZoneEffectTypeData
    id_field = 'zone_effect_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ZoneEffectTypeData:
        return ZoneEffectTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class ZoneEffectData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone_effect.ZoneEffectData`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        zone_effect_id: The unique ID of this zone effect.
        zone_effect_type_id: The ID of the associated
            :class:`ZoneEffectType`.
        ability_id: The :class:`~auraxium.ps2.Ability` associated with
            this zone effect.
        param*: Type-specific parameters for this zone effect. Refer to
            the corresponding :class:`ZoneEffectType` for details.

    """

    zone_effect_id: int
    zone_effect_type_id: int
    ability_id: int
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'ZoneEffectData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(6)]
        return cls(
            int(data['zone_effect_id']),
            int(data['zone_effect_type_id']),
            int(data['ability_id']),
            *params)


class ZoneEffect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect or buff applied by a zone.

    Access the corresponding
    :class:`auraxium.ps2.zone_effect.ZoneEffectType` instance via the
    :meth:`type` method for information on generic parameters.
    """

    collection = 'zone_effect'
    data: ZoneEffectData
    id_field = 'zone_effect_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ZoneEffectData:
        return ZoneEffectData.from_census(data)

    def ability(self) -> InstanceProxy[Ability]:
        """Return the ability associated with this zone effect."""
        query = Query(Ability.collection, service_id=self._client.service_id)
        query.add_term(field=Ability.id_field, value=self.data.ability_id)
        return InstanceProxy(Ability, query, client=self._client)

    def type(self) -> InstanceProxy[ZoneEffectType]:
        """Return the type of this zone effect."""
        query = Query(
            ZoneEffectType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ZoneEffectType.id_field, value=self.data.zone_effect_type_id)
        return InstanceProxy(ZoneEffectType, query, client=self._client)
