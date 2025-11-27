"""Effect and effect type class definitions."""

import enum
from ..base import Cached
from ..census import Query
from ..collections import (EffectData, EffectTypeData, ZoneEffectData,
                      ZoneEffectTypeData)
from .._proxy import InstanceProxy

from ._ability import Ability
from ._resist import ResistType

__all__ = [
    'Effect',
    'EffectType',
    'TargetType',
    'ZoneEffect',
    'ZoneEffectType'
]


class TargetType(enum.IntEnum):
    """Enumerate the types of targets for effects.

    Effects will only act upon entities matching the given target type.
    This is why AoE heal generally does not apply to enemies.

    Values:::

       SELF  = 1
       ANY   = 2
       ENEMY = 3
       ALLY  = 4
    """

    SELF = 1
    ANY = 2
    ENEMY = 3
    ALLY = 4

    def __str__(self) -> str:
        literals = ['Self', 'Any', 'Enemy', 'Ally']
        return literals[int(self.value)]


class EffectType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of effect.

    Effect types specify the core function of a given :class:`Effect`.
    The ``param*`` fields in the effect type list what these generic
    parameters are used for in effects of this type.

    Effects include damage (direct, indirect, and distance falloff),
    (de-)buffs, resource modification, as well as healing/revives.

    .. attribute:: id
       :type: int

       The unique ID of this effect type. In the API payload, this
       field is called ``effect_type_id``.

    .. attribute:: description
       :type: str

       A description of what this effect type is used for.

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
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None


class Effect(Cached, cache_size=10, cache_ttu=60.0):
    """An effect acting on a character.

    Effects are usually created by an :class:`~auraxium.ps2.Ability` or
    are the result of a weapon firing.

    Access the corresponding :class:`EffectType` instance via the
    :meth:`Effect.type` method for information on generic parameters.

    .. note::

       The relationship between :class:`Effect` and :class:`ZoneEffect`
       is currently undocumented and non-obvious.

       Both deal in weapon and character stat modifiers, but
       :class:`Effect` seems to act on individual entities (damage,
       single-target-heal, revives, etc.) while :class:`ZoneEffect`
       usually acts on groups of entities (ammo dispatch, armour buffs,
       etc.).

    .. attribute:: id
       :type: int

       The unique ID of this effect. In the API payload, this field is
       called ``effect_id``.

    .. attribute:: effect_type_id
       :type: int

       The ID of the :class:`EffectType` of this effect.

       .. seealso::

          :meth:`type` -- Return the type of this effect.

    .. attribute:: ability_id
       :type: int | None

       The ability that  the effect, if any.

    .. attribute:: target_type_id
       :type: int | None

       Integer value of the :class:`~auraxium.ps2.TargetType` enum used
       to find targets for this effect.

       .. seealso::

          :meth:`target_type` -- Return the enum value representing the
          effect's target type.

    .. attribute:: resist_type_id
       :type: int

       The :class:`~auraxium.ps2.ResistType` entry used by this effect.

       .. seealso::

          :meth:`resist_type` -- Return the resist type used by this
          effect.

    .. attribute:: is_drain
       :type: bool | None

       Unknown. This flag does not appear to correlate with draineable
       abilities such as Afterburners or overshields.

       The resist type of any effect with this flag set will be zero.

    .. attribute:: duration_seconds
       :type: float | None

       The duration of the effect. For continuously channeled effects
       such as the Combat Medic's healing beam, this will be 999'999
       seconds.

    .. attribute:: param*
       :type: str |None

       Type-specific parameters for this effect. Refer to the
       corresponding :class:`EffectType` for details.
    """

    collection = 'effect'
    data: EffectData
    id_field = 'effect_id'
    _model = EffectData

    # Type hints for data class fallback attributes
    id: int
    effect_type_id: int
    ability_id: int | None
    target_type_id: int | None
    resist_type_id: int
    is_drain: bool | None
    duration_seconds: float | None
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None

    def resist_type(self) -> InstanceProxy[ResistType]:
        """Return the resist type of the effect.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(ResistType.collection,
                      service_id=self._client.service_id)
        query.add_term(field=ResistType.id_field, value=self.resist_type_id)
        return InstanceProxy(ResistType, query, client=self._client)

    def target_type(self) -> TargetType | None:
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
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None


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
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None

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
