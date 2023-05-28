"""Data classes for event streaming service payloads."""

from typing import Optional

from .base import Event, CharacterEvent, WorldEvent

__all__ = [
    'AchievementAdded',
    'BattleRankUp',
    'ContinentLock',
    'Death',
    'FacilityControl',
    'GainExperience',
    'ItemAdded',
    'MetagameEvent',
    'PlayerFacilityCapture',
    'PlayerFacilityDefend',
    'PlayerLogin',
    'PlayerLogout',
    'SkillAdded',
    'VehicleDestroy'
]

# pylint: disable=too-few-public-methods


class AchievementAdded(Event, CharacterEvent):
    """A character has earned a new achievement.

    Achievements are either weapon medals or service ribbons.

    .. attribute:: character_id
       :type: int

       ID of the :class:`~auraxium.ps2.Character` that earned the
       achievement.

    .. attribute:: achievement_id
       :type: int

       ID of the :class:`~auraxium.ps2.Achievement` that was earned.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int
    achievement_id: int
    zone_id: int


class BattleRankUp(Event, CharacterEvent):
    """A character has earned a new battle rank.

    Note that this may not reflect the characters actual new battle
    rank as they may be have joined the A.S.P.

    .. attribute:: battle_rank
       :type: int

       The new battle rank of the character.

    .. attribute:: character_id
       :type: int

       ID of the :class:`~auraxium.ps2.Character` that ranked up.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    battle_rank: int
    character_id: int
    zone_id: int


class Death(Event, CharacterEvent):
    """A character has been killed.

    If the attacker and victim ID are identical, the character has
    killed themselves (e.g. with explosives).

    An attacker ID of ``0`` indicates that the player has died to
    non-player sources like fall damage, or spawn room pain fields.

    .. attribute:: attacker_character_id
       :type: int

       The ID of the killing :class:`~auraxium.ps2.Character`.

    .. attribute:: attacker_fire_mode_id
       :type: int

       ID of the :class:`~auraxium.ps2.FireMode` used.

    .. attribute:: attacker_loadout_id
       :type: int

       ID of the :class:`~auraxium.ps2.Loadout` of the attacker.

    .. attribute:: attacker_vehicle_id
       :type: int

       ID of the :class:`~auraxium.ps2.Vehicle` of the attacker.

    .. attribute:: attacker_weapon_id
       :type: int

       ID of the :class:`~auraxium.ps2.Item` used by the attacker.

       .. important::

         The reference above is not an error, this field reports the
         item ID of the weapon, not the weapon ID.

    .. attribute:: character_id
       :type: int

       ID of the :class:`~auraxium.ps2.Character` that was killed.

    .. attribute:: character_loadout_id
       :type: int

       ID of the :class:`~auraxium.ps2.Loadout` of the victim.

    .. attribute:: is_critical
       :type: bool | None

       Whether the killing blow dealt critical damage.

       .. note::

          This value is always false.

    .. attribute:: is_headshot
       :type: bool

       Whether the killing blow was dealt via headshot.

    .. attribute:: vehicle_id
       :type: int | None

       The type of :class:`~auraxium.ps2.Vehicle` the victim was in at
       the time of death, if any.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    attacker_character_id: int
    attacker_fire_mode_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    character_loadout_id: int
    is_critical: Optional[bool]  # Always false
    is_headshot: bool
    vehicle_id: Optional[int]
    zone_id: int


class FacilityControl(Event, WorldEvent):
    """A facility has switched factions.

    This is generally due to hostile takeover, but is also dispatched
    when a coninent is locked or unlocked server-side (e.g. due to an
    alert ending).

    .. attribute:: duration_held
       :type: int

       The amount of time the base was in the old faction's ownership
       in seconds.

    .. attribute:: facility_id
       :type: int

       The facility ID of the base.

    .. attribute:: new_faction_id
       :type: int

       ID of the new :class:`~auraxium.ps2.Faction`.

    .. attribute:: old_faction_id
       :type: int

       ID of the old :class:`~auraxium.ps2.Faction`.

    .. attribute:: outfit_id
       :type: int

       ID of the :class:`~auraxium.ps2.Outfit` that was awarded the
       base capture.

    .. attribute:: zone_id
       :type: int

       The :class:`~auraxium.ps2.Zone` of the captured base.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    duration_held: int
    facility_id: int
    new_faction_id: int
    old_faction_id: int
    outfit_id: int
    zone_id: int


class GainExperience(Event, CharacterEvent):
    """A character has gained a tick of experience.

    .. attribute:: amount
       :type: int

       The amount of experience gained.

    .. attribute:: character_id
       :type: int

       ID of the :class:`~auraxium.ps2.Character` that earned
       experience.

    .. attribute:: experience_id
       :type: int

       The source of the experience gain.

       .. note::

          Not all types of experience gain have a cooresponding
          :class:`~auraxium.ps2.Experience` entry.

    .. attribute:: loadout_id
       :type: int

       The current :class:`~auraxium.ps2.Loadout` of the character.

    .. attribute:: other_id
       :type: int

       The ID of another entity involved in the experience acquisition.
       For heals, this would be the healed ally, for spots the enemy
       vehicle or player spottet, etc.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    amount: int
    character_id: int
    experience_id: int
    loadout_id: int
    other_id: int
    zone_id: int

    @classmethod
    def filter_experience(cls, id_: int) -> str:
        """Factory for custom, experience ID specific events.

        This method is used to generate custom event names that allow
        only subscribing to a single type of experience gain. The
        returned string can be passed to a
        :class:`auraxium.event.Trigger`.

        :param int id_: The experience ID to subscribe to.
        :return: A custom event name for the given experience type.
        """
        return f'{cls.__name__}_experience_id_{id_}'


class ItemAdded(Event, CharacterEvent):
    """A character has been granted an item.

    This includes internal flags and invisible items used to control
    outfit resources and war assets.

    .. attribute:: character_id
       :type: int

       ID of the character that has been awarded an item.

    .. attribute:: context
       :type: str

       The reason or mechanic that led to the item being awarded.
       Notably, this includes outfit resource use.

    .. attribute:: item_count
       :type: str

       The number of items that were added.

    .. attribute:: item_id
       :type: int

       The :class:`~auraxium.ps2.Item` that was added.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int
    context: str
    item_count: int
    item_id: int
    zone_id: int


class MetagameEvent(Event, WorldEvent):
    """A metagame event (i.e. alert) has changed state.

    .. attribute:: experience_bonus
       :type: int

       The experience bonus applied for the duration of the event
       (a value of 25 denotes a 25% experience bonus for all
       participants)

    .. attribute:: faction_nc
       :type: float

       The current event score of the NC.

    .. attribute:: faction_tr
       :type: float

       The current event score of the TR.

    .. attribute:: faction_vs
       :type: float

       The current event score of the NC.

    .. attribute:: metagame_event_id
       :type: int

       ID of the :class:`~auraxium.ps2.MetagameEvent` that changed
       state.

    .. attribute:: metagame_event_state
       :type: int

       The new :class:`~auraxium.ps2.MetagameEventState` of the event.

    .. attribute:: zone_id
       :type: int

       The :class:`~auraxium.ps2.Zone` the event is taking place in.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    experience_bonus: float
    faction_nc: float
    faction_tr: float
    faction_vs: float
    instance_id: int
    metagame_event_id: int
    metagame_event_state: int
    metagame_event_state_name: str
    # This default value is a sentinel to inform the validator that this field
    # has not been provided.
    zone_id: int = -1


class PlayerFacilityCapture(Event, CharacterEvent):
    """A player has participated in capturing a facility.

    .. attribute:: character_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Character` that participated
       in the capture.

    .. attribute:: facility_id
       :type: int

       ID of the facility that was captured.

    .. attribute:: outfit_id
       :type: int

       The :class:`~auraxium.ps2.Outfit` that was awarded the facility.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int
    facility_id: int
    outfit_id: int
    zone_id: int


class PlayerFacilityDefend(Event, CharacterEvent):
    """A player has participated in defending a facility.

    .. attribute:: character_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Character` that participated
       in the defence.

    .. attribute:: facility_id
       :type: int

       ID of the facility that was defended.

    .. attribute:: outfit_id
       :type: int

       The :class:`~auraxium.ps2.Outfit` that currently owns the
       facility.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int
    facility_id: int
    outfit_id: int
    zone_id: int


class PlayerLogin(Event, CharacterEvent, WorldEvent):
    """A player has logged into the game.

    .. attribute:: character_id
       :type: int

       The :class:`~auraxium.ps2.Character` that logged in.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int


class PlayerLogout(Event, CharacterEvent, WorldEvent):
    """A player has logged out.

    .. attribute:: character_id
       :type: int

       The :class:`~auraxium.ps2.Character` that logged off.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int


class SkillAdded(Event, CharacterEvent):
    """A player has unlocked a skill (i.e. certification or ASP).

    .. attribute:: character_id
       :type: int

       The :class:`~auraxium.ps2.Character` that gained a new skill.

    .. attribute:: skill_id
       :type: int

       The :class:`~auraxium.ps2.Skill` the character unlocked.

    .. attribute:: zone_id
       :type: int

       The current :class:`~auraxium.ps2.Zone` of the character.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    character_id: int
    skill_id: int
    zone_id: int


class VehicleDestroy(Event, CharacterEvent):
    """A player's vehicle has been destroyed.

    .. attribute:: attacker_character_id
       :type: int

       The ID of the killing :class:`~auraxium.ps2.Character`.

    .. attribute:: attacker_loadout_id
       :type: int

       ID of the :class:`~auraxium.ps2.Loadout` of the attacker.

    .. attribute:: attacker_vehicle_id
       :type: int

       ID of the :class:`~auraxium.ps2.Vehicle` of the attacker.

    .. attribute:: attacker_weapon_id
       :type: int

       ID of the :class:`~auraxium.ps2.Item` used by the attacker.

       .. important::

         The reference above is not an error, this field reports the
         item ID of the weapon, not the weapon ID.

    .. attribute:: character_id
       :type: int

       ID of the :class:`~auraxium.ps2.Character` that was killed.

    .. attribute:: facility_id
       :type: int

       ID of the facility the vehicle was destroyed at.

       .. note::

          As of March 2021, this field is only populated for destroyed
          base turrets. All other vehicles do not contain facility
          data.

    .. attribute:: faction_id
       :type: int

       The :class:`~auraxium.ps2.Faction` of the vehicle.

    .. attribute:: vehicle_id
       :type: int | None

       The type of :class:`~auraxium.ps2.Vehicle` that was destroyed.

    .. attribute:: zone_id
       :type: int

       The :class:`~auraxium.ps2.Zone` the vehicle was destroyed in.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    attacker_character_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    facility_id: int
    faction_id: int
    vehicle_id: int
    zone_id: int


class ContinentLock(Event, WorldEvent):
    """A continent has been locked.

    .. attribute:: zone_id
       :type: int

       ID of the :class:`~auraxium.ps2.Zone` that was locked.

    .. attribute:: triggering_faction
       :type: int

       The faction that triggered the meltdown alert.

    .. attribute:: previous_faction
       :type: int

       The faction that has previously held this continent.

    .. attribute:: vs_population
       :type: float

       Population percentage for VS.

    .. attribute:: nc_population
       :type: float

       Population percentage for NC.

    .. attribute:: tr_population
       :type: float

       Population percentage for TR.

    .. attribute:: metagame_event_id
       :type: int

       The ID of the :class:`~auraxium.ps2.MetagameEvent` that caused
       the continent to lock.

    .. attribute:: timestamp
       :type: int

       The UTC timestamp of the event. May be used to infer latency to
       the event streaming endpoint.

    .. attribute:: world_id
       :type: int

       ID of the :class:`~auraxium.ps2.World` whose event streaming
       endpoint broadcast the event.
    """

    zone_id: int
    triggering_faction: int
    previous_faction: int
    vs_population: float
    nc_population: float
    tr_population: float
    metagame_event_id: int
