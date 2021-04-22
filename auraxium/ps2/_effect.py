"""Effect and effect type class definitions."""

import enum
from typing import Optional

from ..base import Cached
from ..census import Query
from ..models import (EffectData, EffectTypeData, ZoneEffectData,
                      ZoneEffectTypeData)
from .._proxy import InstanceProxy

from ._ability import Ability

__all__ = [
    'Effect',
    'EffectType',
    'TargetType',
    'ZoneEffect',
    'ZoneEffectType'
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


    .. attribute:: id
       :type: int

       The unique ID of this effect type.


    .. attribute:: description
       :type: str

       A description of what this effect type is used  for.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       effects of this type.
    """

    collection = 'effect_type'
    data: EffectTypeData
    id_field = 'effect_type_id'
    _model = EffectTypeData

    # Type hints for data class fallback attributes
    id: int
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

    Access the corresponding :class:`~auraxium.ps2.EffectType` instance
    via the :meth:`Effect.type` method for information on generic
    parameters.

    .. attribute:: id
       :type: int

       The unique ID of this effect.

    .. attribute:: effect_type_id
       :type: int

       The associated effect type for this effect.

    .. attribute:: ability_id
       :type: int | None

       The ability spawning the effect, if any.

    .. attribute:: target_type_id
       :type: int | None

       Integer value of the :class:`~auraxium.ps2.TargetType` enum used
       to find targets for this effect.

    .. attribute:: resist_type_id
       :type: int

       The :class:`~auraxium.ps2.ResistInfo` entry used by this effect.

    .. attribute:: is_drain
       :type: bool | None

       (Not yet documented)

    .. attribute:: duration_seconds
       :type: float | None

       The duration of the effect.

    .. attribute:: param*
       :type: str |None

       Type-specific parameters for this effect. Refer to the
       corresponding :class:`~auraxium.ps2.EffectType` for details.
    """

    collection = 'effect'
    data: EffectData
    id_field = 'effect_id'
    _model = EffectData

    # Type hints for data class fallback attributes
    id: int
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


class ZoneEffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of zone effect.

    Zone effect types specify the core function of a given
    :class:`ZoneEffect`. The ``param*`` fields in the zone effect type
    list what these generic parameters are used for in effects of this
    type.

    .. attribute:: id
       :type: int

       The unique ID of this zone effect type. In the API payload, this
       field is called ``zone_effect_type_id``.

    .. attribute:: description
       :type: str

       A description of what this zone effect type is used for.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       zone effects of this type.
    """

    collection = 'zone_effect_type'
    data: ZoneEffectTypeData
    id_field = 'zone_effect_type_id'
    _model = ZoneEffectTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]


class ZoneEffect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect or buff applied in an area.

    Zone effects are area-bound effects acting on a group of characters
    or entities.

    Access the corresponding :class:`ZoneEffectType` instance via the
    :meth:`type` method for information on generic parameters.

    .. note::

       The relationship between :class:`ZoneEffect` and :class:`Effect`
       is currently undocumented and non-obvious.

       Both deal in weapon and character stat modifiers, but
       :class:`Effect` seems to act on individual entities (damage,
       single-target-heal, revives, etc.) while :class:`ZoneEffect`
       usually acts on groups of entities (ammo dispatch, armour buffs,
       etc.).

       However, zone effects are also responsible for Gate Shield
       Diffusors and certain types of implant buffs like the jump
       height of Catlike. Again, more information is needed here.

    .. attribute:: id
       :type: int

       The unique ID of this zone effect. In the API payload, this
       field is called ``zone_effect_id``.

    .. attribute:: zone_effect_type_id
       :type: int

       The ID of the associated :class:`ZoneEffectType`.

       .. seealso::

          :meth:`type` -- Return the type of this effect.

    .. attribute:: ability_id
       :type: int

       The ID of the :class:`auraxium.ps2.Ability` associated with this
       zone effect.

       .. note::

          Tests are inconclusive whether this is the ability that
          triggered the zone effect or whether these effects are used
          to control abilities.

       .. seealso::

          :meth:`ability` -- The ability associated with this zone
          effect.

    .. attribute:: param*
       :type: str | None

       Type-specific parameters for this zone effect. Refer to the
       corresponding :class:`ZoneEffectType` for details.
    """

    collection = 'zone_effect'
    data: ZoneEffectData
    id_field = 'zone_effect_id'
    _model = ZoneEffectData

    # Type hints for data class fallback attributes
    id: int
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
