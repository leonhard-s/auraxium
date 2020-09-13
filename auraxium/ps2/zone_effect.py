"""Ability and ability type class definitions."""

from ..base import Cached
from ..census import Query
from ..models import ZoneEffectData, ZoneEffectTypeData
from ..proxy import InstanceProxy
from ..types import CensusData

from .ability import Ability


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
