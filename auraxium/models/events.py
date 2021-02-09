"""Data classes for event streaming service payloads."""

import warnings
from typing import Any, Dict

import pydantic

from ..event import Event

__all__ = [
    'AchievementAdded',
    'BattleRankUp',
    'ContinentLock',
    'ContinentUnlock',
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

# Backup mapping of metagame_event_id to zone_id
_EVENT_TO_ZONE: Dict[int, int] = {
    # VS meltdown
    157: 2, 154: 4, 148: 6, 151: 8,
    # VS unstable meltdown
    189: 2, 187: 4, 188: 6, 186: 8,
    # NC meltdown
    158: 2, 155: 4, 149: 6, 152: 8,
    # NC unstable meltdown
    179: 2, 177: 4, 178: 6, 176: 8,
    # TR meltdown
    156: 2, 153: 4, 147: 6, 150: 8,
    # TR unstable meltdown
    193: 2, 191: 4, 192: 6, 190: 8,
    # Warpgates stabilizing
    160: 2, 162: 4, 159: 6, 161: 8
}


class AchievementAdded(Event):
    """A character has earned a new achievement.

    Achievements are either weapon medals or service ribbons.
    """

    character_id: int
    achievement_id: int
    zone_id: int


class BattleRankUp(Event):
    """A character has earned a new battle rank.

    Note that this may not reflect the characters actual new battle
    rank as they may be have joined the A.S.P.
    """

    battle_rank: int
    character_id: int
    zone_id: int


class Death(Event):
    """A character has been killed.

    If the attacker and victim ID are identical, the character has
    killed themselves (e.g. with explosives).

    An attacker ID of ``0`` indicates that the player has died to
    non-player sources like fall damage, or spawn room pain fields.
    """

    attacker_character_id: int
    attacker_fire_mode_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    character_loadout_id: int
    is_critical: bool  # Always false
    is_headshot: bool
    vehicle_id: int
    zone_id: int


class FacilityControl(Event):
    """A facility has switched factions.

    This is generally due to hostile takeover, but is also dispatched
    when a coninent is locked or unlocked server-side (e.g. due to an
    alert ending).
    """

    duration_held: int
    facility_id: int
    new_faction_id: int
    old_faction_id: int
    outfit_id: int
    zone_id: int


class GainExperience(Event):
    """A character has gained a tick of experience."""

    amount: int
    character_id: int
    experience_id: int
    loadout_id: int
    other_id: int
    zone_id: int


class ItemAdded(Event):
    """A character has been granted an item.

    This includes internal flags and invisible items used to control
    outfit resources and war assets.
    """

    character_id: int
    context: str
    item_count: int
    item_id: int
    zone_id: int


class MetagameEvent(Event):
    """A metagame event (i.e. alert) has changed state."""

    experience_bonus: int
    faction_nc: float
    faction_tr: float
    faction_vs: float
    metagame_event_id: int
    metagame_event_state: int
    # This default value is a sentinel to inform the validator that this field
    # has not been provided.
    zone_id: int = -1

    @pydantic.root_validator
    @classmethod
    def _insert_zone_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Restore the missing ``zone_id`` field.

        As of creating this module, the ``zone_id`` field has been
        missing from payloads for years. This validator restores it
        using the :attr:`metagame_event_id` field of the payload.

        This is hard-coded and prone to breaking with updates, which is
        why this validator will always try to use the provided value
        and only use the local lookup table if it wasn't found.

        If the local table does not support the given
        :attr:`metagame_event_id`, a warning is raised and ``zone_id``
        set to ``0``.
        """
        if values['zone_id'] < 0:
            event_id = int(values['metagame_event_id'])
            try:
                values['zone_id'] = _EVENT_TO_ZONE[event_id]
            except KeyError:
                values['zone_id'] = 0
                warnings.warn('Unable to infer zone_id from unknown alert '
                              f'type {event_id}, zone_id has been set to 0')
        return values


class PlayerFacilityCapture(Event):
    """A player has participated in capturing a facility."""

    character_id: int
    facility_id: int
    outfit_id: int
    zone_id: int


class PlayerFacilityDefend(Event):
    """A player has participated in defending a facility."""

    character_id: int
    facility_id: int
    outfit_id: int
    zone_id: int


class PlayerLogin(Event):
    """A player has logged into the game."""

    character_id: int


class PlayerLogout(Event):
    """A player has logged out."""

    character_id: int
    event_name: str


class SkillAdded(Event):
    """A player has unlocked a skill (i.e. certification or ASP)."""

    character_id: int
    skill_id: int
    zone_id: int


class VehicleDestroy(Event):
    """A player's vehicle has been destroyed."""

    attacker_character_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    facility_id: int  # broken
    faction_id: int
    vehicle_id: int
    zone_id: int


class ContinentLock(Event):
    """A continent has been locked."""
    zone_id: int
    triggering_faction: int
    previous_faction: int
    vs_population: float
    nc_population: float
    tr_population: float
    metagame_event_id: int
    event_type: int


class ContinentUnlock(Event):
    """A continent has been unlocked."""
    zone_id: int
    triggering_faction: int
    previous_faction: int
    vs_population: float
    nc_population: float
    tr_population: float
    metagame_event_id: int
    event_type: int
