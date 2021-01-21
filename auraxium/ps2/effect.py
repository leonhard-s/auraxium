"""Effect and effect type class definitions."""

import enum
from typing import Optional

from .._base import Cached
from ..census import Query
from ..models import EffectData, EffectTypeData
from .._proxy import InstanceProxy

__all__ = [
    'Effect',
    'EffectType',
    'TargetType'
]


class TargetType(enum.IntEnum):
    """Enumerate the types of targets for effects."""

    SELF = 1
    ANY = 2
    ENEMY = 3
    ALLY = 4


class EffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of effect.

    This class mostly specifies the purpose of any generic parameters.

    Attributes:
        effect_type_id: The unique ID of this effect type.
        description: A description of what this effect type is used
            for.
        param*: Descriptions of what the corresponding parameter is
            used for in abilities of this type.

    """

    collection = 'effect_type'
    data: EffectTypeData
    dataclass = EffectTypeData
    id_field = 'effect_type_id'

    # Type hints for data class fallback attributes
    effect_type_id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]


class Effect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect acting on a character.

    Access the corresponding :class:`auraxium.ps2.effect.EffectType`
    instance via the :meth:`type` method for information on generic
    parameters.

    Attributes:
        effect_id: The unique ID of this effect.
        effect_type_id: The associated effect type for this effect.
        ability_id: The ability spawning the effect, if any.
        target_type_id: Integer value of the :class:`TargetType`
            enumerator used to find targets for this effect.
        resist_type_id: The :class:`~auraxium.ps2.ResistInfo` entry
            used by this effect.
        is_drain: (Not yet documented)
        duration_seconds: The duration of the effect.
        param*: Type-specific parameters for this effect. Refer to the
            corresponding :class:`EffectType` for details.

    """

    collection = 'effect'
    data: EffectData
    dataclass = EffectData
    id_field = 'effect_id'

    # Type hints for data class fallback attributes
    effect_id: int
    effect_type_id: int
    ability_id: Optional[int]
    target_type_id: Optional[int]
    resist_type_id: int
    is_drain: Optional[bool]
    duration_seconds: Optional[float]
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]

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
