"""Contains object representations of the PlanetSide 2 (PC) event types.

All classed defined herein are subclassed to the "Event" class. They are all
created by feeding them with the "payload" dictionary received by the event
streaming service.
"""

from ..base_api import Query
from ..object_models.ps2 import (Achievement, Alert, AlertState, Character, Experience, Faction,
                                 FireMode, Item, Loadout, Outfit, Region, Skill, Vehicle, Weapon,
                                 World, Zone)

from .events import Event


class AchievementEarned(Event):
    """A character has earned an achievement (weapon medal or service ribbon).

    (This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.achievement_id = int(payload['achievement_id'])
        self.character_id = int(payload['character_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def achievement(self) -> Achievement:
        return Achievement.get(id=self.achievement_id)

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def world_id(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone_id(self) -> Zone:
        return Zone.get(id=self.zone_id)


class BattleRankUp(Event):
    """A character has earned a battle rank (i.e. levelled up).

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.battle_rank = payload['battle_rank']
        self.character_id = payload['character_id']

        self.world_id = payload['world_id']
        self.zone_id = payload['zone_id']

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class ContinentLock(Event):  # pylint: disable=too-many-instance-attributes
    """A continent has been locked (i.e. captured by a faction).

    This is a world-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.metagame_event_id = int(payload['metagame_event_id'])
        self.metagame_event_type = payload['event_type']
        self.population_nc = payload['nc_population']
        self.population_tr = payload['tr_population']
        self.population_vs = payload['vs_population']
        self.previous_faction_id = int(payload['previous_faction'])
        self.triggering_faction_id = int(payload['triggering_faction'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def metagame_event(self) -> Alert:
        return Alert.get(id=self.metagame_event_id)

    @property
    def previous_faction(self) -> Faction:
        return Faction.get(id=self.previous_faction_id)

    @property
    def triggering_faction(self) -> Faction:
        return Faction.get(id=self.triggering_faction_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class ContinentUnlock(Event):  # pylint: disable=too-many-instance-attributes
    """A continent has been unlocked.

    This is a world-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.metagame_event_id = int(payload['metagame_event_id'])
        self.metagame_event_type = int(payload['event_type'])
        self.population_nc = payload['nc_population']
        self.population_tr = payload['tr_population']
        self.population_vs = payload['vs_population']
        self.previous_faction_id = int(payload['previous_faction'])
        self.triggering_faction_id = int(payload['triggering_faction'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def metagame_event(self) -> Alert:
        return Alert.get(id=self.metagame_event_id)

    @property
    def previous_faction(self) -> Faction:
        return Faction.get(id=self.previous_faction_id)

    @property
    def triggering_faction(self) -> Faction:
        return Faction.get(id=self.triggering_faction_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class Death(Event):  # pylint: disable=too-many-instance-attributes
    """A character has died or been killed.

    This event will be sent regardless of whether the tracked player is the
    victim or the killer.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.attacker_id = int(payload['attacker_character_id'])
        self.attacker_fire_mode_id = int(payload['attacker_fire_mode_id'])
        self.attacker_loadout_id = int(payload['attacker_loadout_id'])
        self.attacker_vehicle_id = int(payload['attacker_vehicle_id'])
        self.attacker_weapon_id = int(payload['attacker_weapon_id'])
        self.is_critical = payload['is_critical']
        self.is_headshot = int(payload['is_headshot'])
        self.victim_id = int(payload['character_id'])
        self.victim_loadout_id = int(payload['loadout_id'])
        self.victim_vehicle_id = int(payload['vehicle_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def attacker(self) -> Character:
        return Character.get(id=self.attacker_id)

    @property
    def attacker_fire_mode(self) -> FireMode:
        return FireMode.get(id=self.attacker_fire_mode_id)

    @property
    def attacker_loadout(self) -> Loadout:
        return Loadout.get(id=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Weapon:
        return Weapon.get(id=self.attacker_weapon_id)

    @property
    def victim(self) -> Character:
        return Character.get(id=self.victim_id)

    @property
    def victim_loadout(self) -> Loadout:
        return Loadout.get(id=self.victim_loadout_id)

    @property
    def victim_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.victim_vehicle_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class FacilityControl(Event):  # pylint: disable=too-many-instance-attributes
    """A facility has changed ownership.

    This is a world-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.duration_held = int(payload['duration_held'])
        self.facility_id = int(payload['facility_id'])
        self.new_faction_id = int(payload['new_faction_id'])
        self.old_faction_id = int(payload['old_faction_id'])
        self.outfit_id = int(payload['outfit_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def region(self) -> Region:
        from .. import namespace
        q = Query('map_region', namespace=namespace, facility_id=self.facility_id)
        q.join('region', inject_at='region', on='map_region_id', to='region_id')
        data = q.get(single=True)['region']
        return Region.get(id=self.facility_id, data=data)

    @property
    def new_faction(self) -> Faction:
        return Faction.get(id=self.new_faction_id)

    @property
    def old_faction(self) -> Faction:
        return Faction.get(id=self.old_faction_id)

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class GainExperience(Event):
    """A character has earned experience.

    This is a very common event that should be used with care. It can create a
    very large number of hits, even for a moderate list of tracked players.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.amount = int(payload['amount'])
        self.character_id = int(payload['character_id'])
        self.experience_id = int(payload['experience_id'])
        self.loadout_id = int(payload['loadout_id'])
        self.other_id = int(payload['other_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def experience(self) -> Experience:
        return Experience.get(id=self.experience_id)

    @property
    def loadout(self) -> Loadout:
        return Loadout.get(id=self.loadout_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class ItemAdded(Event):
    """A character has received an item.

    Sent when a player receives or unlocks an item, an implant drop or when
    cosmetics are granted to a player.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.context = int(payload['context'])
        self.item_count = int(payload['item_count'])
        self.item_id = int(payload['item_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def item(self) -> Item:
        return Item.get(id=self.item_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class MetagameEvent(Event):  # pylint: disable=too-many-instance-attributes
    """An event or alert has started or ended.

    This is a world-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.experience_bonus = int(payload['experience_bonus'])
        self.faction_nc = int(payload['faction_nc'])
        self.faction_tr = int(payload['faction_tr'])
        self.faction_vs = int(payload['faction_vs'])
        self.metagame_event_id = int(payload['metagame_event_id'])
        self.metagame_event_state = int(payload['metagame_event_state'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def metagame_event(self) -> Alert:
        return Alert.get(id=self.metagame_event_id)

    @property
    def metagame_event_state(self) -> AlertState:
        return AlertState.get(id=self.metagame_event_state)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class PlayerFacilityCapture(Event):
    """A character has participated in capturing a facility.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.facility_id = int(payload['facility_id'])
        self.outfit_id = int(payload['outfit_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def facility(self) -> Faction:
        return Region.get(id=self.facility_id)

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class PlayerFacilityDefend(Event):
    """A character has participated in defending a facility.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.facility_id = int(payload['facility_id'])
        self.outfit_id = int(payload['outfit_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def facility(self) -> Region:
        return Region.get(id=self.facility_id)

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class PlayerLogin(Event):
    """A character has logged into their account.

    This event is both character-centric and world-centric.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.world_id = int(payload['world_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)


class PlayerLogout(Event):
    """A character has logged out of their account.

    This event is both character-centric and world-centric.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.world_id = int(payload['world_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)


class SkillAdded(Event):
    """A character has unlocked or been granted a skill (certification).

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.skill_id = int(payload['skill_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)

    @property
    def skill(self) -> Skill:
        return Skill.get(id=self.skill_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)


class VehicleDestroy(Event):  # pylint: disable=too-many-instance-attributes
    """A vehicle has been destroyed in combat.

    This event will be sent regardless of whether the tracked player is the
    owner or the attacker.

    This is a character-centric event.
    """

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.attacker_id = int(payload['attacker_character_id'])
        self.attacker_loadout_id = int(payload['attacker_loadout_id'])
        self.attacker_vehicle_id = int(payload['attacker_vehicle_id'])
        self.attacker_weapon_id = int(payload['attacker_weapon_id'])
        self.facility_id = int(payload['facility_id'])
        self.faction_id = int(payload['faction_id'])
        self.victim_id = int(payload['character_id'])
        self.victim_vehicle_id = int(payload['vehicle_id'])
        self.world_id = int(payload['world_id'])
        self.zone_id = int(payload['zone_id'])

    @property
    def attacker(self) -> Character:
        return Character.get(id=self.attacker_id)

    @property
    def attacker_loadout(self) -> Loadout:
        return Loadout.get(id=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Weapon:
        return Weapon.get(id=self.attacker_weapon_id)

    @property
    def facility(self) -> Region:
        return Region.get(id=self.facility_id)

    @property
    def faction(self) -> Faction:
        return Faction.get(id=self.faction_id)

    @property
    def victim(self) -> Character:
        return Character.get(id=self.victim_id)

    @property
    def victim_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.victim_vehicle_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
