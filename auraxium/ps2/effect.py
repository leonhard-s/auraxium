"""Effect and effect type class definitions."""

import enum
from typing import Optional

from ..base import Cached
from ..census import Query
from ..models import EffectData, EffectTypeData
from ..proxy import InstanceProxy


class TargetType(enum.IntEnum):
    """Enumerate the types of targets for effects."""

    SELF = 1
    ANY = 2
    ENEMY = 3
    ALLY = 4


class EffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of effect.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'effect_type'
    data: EffectTypeData
    dataclass = EffectTypeData
    id_field = 'effect_type_id'


class Effect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect acting on a character.

    Access the corresponding :class:`auraxium.ps2.effect.EffectType`
    instance via the :meth:`type` method for information on generic
    parameters.
    """

    collection = 'effect'
    data: EffectData
    dataclass = EffectData
    id_field = 'effect_id'

    def target_type(self) -> Optional[TargetType]:
        """Return the target type of this effect."""
        if self.data.target_type_id is None:
            return None
        return TargetType(self.data.target_type_id)

    def type(self) -> InstanceProxy[EffectType]:
        """Return the effect type of this effect."""
        query = Query(
            EffectType.collection, service_id=self._client.service_id)
        query.add_term(
            field=EffectType.id_field, value=self._client.service_id)
        return InstanceProxy(EffectType, query, client=self._client)
