from typing import Literal, Optional

__all__ = [
    "AchievementEarned",
    "BattleRankUp",
    "Death",
    "GainExperience",
    "ItemAdded",
    "PlayerFacilityCapture",
    "PlayerFacilityDefend",
    "PlayerLogin",
    "PlayerLogout",
    "SkillAdded",
    "VehicleDestroy"
]

from ..event import Event


class AchievementEarned(Event):
    event_name: Literal['AchievementEarned']
    achievement_id: int
    character_id: int


class BattleRankUp(Event):
    event_name: Literal['BattleRankUp']
    battle_rank: int
    character_id: int


class Death(Event):
    event_name: Literal['Death']
    attacker_character_id: int
    attacker_fire_mode_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    character_loadout_id: int
    is_critical: Optional[bool]
    is_headshot: bool
    vehicle_id: Optional[int]


class GainExperience(Event):
    event_name: Literal['GainExperience']
    amount: int
    character_id: int
    experience_id: int
    loadout_id: int
    other_id: int


class ItemAdded(Event):
    event_name: Literal['ItemAdded']
    character_id: int
    context: str
    item_count: int
    item_id: int


class PlayerFacilityCapture(Event):
    event_name: Literal['PlayerFacilityCapture']
    character_id: int
    facility_id: int
    outfit_id: int


class PlayerFacilityDefend(Event):
    event_name: Literal['PlayerFacilityDefend']
    character_id: int
    facility_id: int
    outfit_id: int


class PlayerLogin(Event):
    event_name: Literal['PlayerLogin']
    character_id: int


class PlayerLogout(Event):
    event_name: Literal['PlayerLogin']
    character_id: int


class SkillAdded(Event):
    event_name: Literal['SkillAdded']
    character_id: int

    skill_id: int


class VehicleDestroy(Event):
    attacker_character_id: int
    attacker_loadout_id: int
    attacker_vehicle_id: int
    attacker_weapon_id: int
    character_id: int
    event_name: Literal['VehicleDestroy']
    facility_id: int
    faction_id: int
    vehicle_id: int
