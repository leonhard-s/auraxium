"""Ability and ability type class definitions."""

from typing import Optional
from .._base import Cached
from ..census import Query
from ..models import ZoneEffectData, ZoneEffectTypeData
from ..proxy import InstanceProxy

from .ability import Ability

__all__ = [
    'ZoneEffect',
    'ZoneEffectType'
]


class ZoneEffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of zone effect.

    This class mostly specifies the purpose of any generic parameters.

    Attributes:
        zone_effect_type_id: The unique ID of this zone effect type.
        description: A description of what this zone effect type is
            used for.
        param*: Descriptions of what the corresponding parameter is
            used for in zone effects of this type.

    """

    collection = 'zone_effect_type'
    data: ZoneEffectTypeData
    dataclass = ZoneEffectTypeData
    id_field = 'zone_effect_type_id'

    # Type hints for data class fallback attributes
    zone_effect_type_id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]


class ZoneEffect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect or buff applied by a zone.

    Access the corresponding
    :class:`auraxium.ps2.zone_effect.ZoneEffectType` instance via the
    :meth:`type` method for information on generic parameters.

    Attributes:
        zone_effect_id: The unique ID of this zone effect.
        zone_effect_type_id: The ID of the associated
            :class:`ZoneEffectType`.
        ability_id: The :class:`~auraxium.ps2.Ability` associated with
            this zone effect.
        param*: Type-specific parameters for this zone effect. Refer to
            the corresponding :class:`ZoneEffectType` for details.

    """

    collection = 'zone_effect'
    data: ZoneEffectData
    dataclass = ZoneEffectData
    id_field = 'zone_effect_id'

    # Type hints for data class fallback attributes
    zone_effect_id: int
    zone_effect_type_id: int
    ability_id: int
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]

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
