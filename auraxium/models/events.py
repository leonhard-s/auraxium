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
    zone_id: int  # missing


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
