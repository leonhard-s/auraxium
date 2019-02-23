"""Contains object representations of the PlanetSide 2 event types.

All classed defined herein are subclassed to the "Event" class. They
are all created by feeding them with the "payload" dictionary received
by the event streaming service.
"""

from typing import Optional

from .. import Query
from ..object_models.ps2 import (Achievement, Alert, AlertState, Character, Experience, Faction,
                                 FireMode, Item, Loadout, Outfit, Region, Skill, Vehicle, Weapon,
                                 World, Zone)

from .events import Event


class AchievementEarned(Event):
    """A character has earned an achievement (weapon medal or service ribbon).

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'AchievementEarned'
    event_name = 'achievement_earned'
    event_type = 0

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
        """The Achievement the character has earned."""
        return Achievement.get(id_=self.achievement_id)

    @property
    def character(self) -> Character:
        """The Character that earned the achievement."""
        return Character.get(id_=self.character_id)

    @property
    def world(self) -> World:
        """The World (server) the achievement was earned on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the achievement was earned on."""
        return Zone.get(id_=self.zone_id)


class BattleRankUp(Event):
    """A character has earned a battle rank (i.e. levelled up).

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'BattleRankUp'
    event_name = 'battle_rank_up'
    event_type = 1

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
        """The Character that earned a battle rank."""
        return Character.get(id_=self.character_id)

    @property
    def world(self) -> World:
        """The World (server) the battle rank was earned on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the battle rank was earned on."""
        return Zone.get(id_=self.zone_id)


class ContinentLock(Event):  # pylint: disable=too-many-instance-attributes
    """A continent has been locked (i.e. captured by a faction).

    This is a world-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'ContinentLock'
    event_name = 'continent_lock'
    event_type = 2

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
        """The Alert that locked the continent."""
        return Alert.get(id_=self.metagame_event_id)

    @property
    def previous_faction(self) -> Faction:
        """The Faction that owned the continent until now."""
        return Faction.get(id_=self.previous_faction_id)

    @property
    def triggering_faction(self) -> Faction:
        """The Faction that captured the continent."""
        return Faction.get(id_=self.triggering_faction_id)

    @property
    def world(self) -> World:
        """The World (server) the continent was locked on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) that was locked."""
        return Zone.get(id_=self.zone_id)


class ContinentUnlock(Event):  # pylint: disable=too-many-instance-attributes
    """A continent has been unlocked.

    This is a world-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'ContinentUnlock'
    event_name = 'continent_unlock'
    event_type = 3

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
        """The Alert that unlocked the continent."""
        return Alert.get(id_=self.metagame_event_id)

    @property
    def previous_faction(self) -> Faction:
        """No information known."""
        return Faction.get(id_=self.previous_faction_id)

    @property
    def triggering_faction(self) -> Faction:
        """No information known."""
        return Faction.get(id_=self.triggering_faction_id)

    @property
    def world(self) -> World:
        """The World (server) the continent was unlocked on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) that was unlocked."""
        return Zone.get(id_=self.zone_id)


class Death(Event):  # pylint: disable=too-many-instance-attributes
    """A character has died or been killed.

    This event will be sent regardless of whether the tracked player is the
    victim or the killer.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'Death'
    event_name = 'death'
    event_type = 4

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
        """The Character that killed the victim."""
        return Character.get(id_=self.attacker_id)

    @property
    def attacker_fire_mode(self) -> FireMode:
        """The FireMode used to kill the victim."""
        return FireMode.get(id_=self.attacker_fire_mode_id)

    @property
    def attacker_loadout(self) -> Loadout:
        """The Loadout the killing player was using."""
        return Loadout.get(id_=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self) -> Optional[Vehicle]:
        """The Vehicle the killing player was in.

        Might be None.
        """
        return Vehicle.get(id_=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Optional[Weapon]:
        """The Weapon used to kill the player.

        Might be None.
        """
        return Weapon.get(id_=self.attacker_weapon_id)

    @property
    def victim(self) -> Character:
        """The Character that has died."""
        return Character.get(id_=self.victim_id)

    @property
    def victim_loadout(self) -> Loadout:
        """The Loadout the victim was using."""
        return Loadout.get(id_=self.victim_loadout_id)

    @property
    def victim_vehicle(self) -> Optional[Vehicle]:
        """The Vehicle the victim was in.

        Might be None.
        """
        return Vehicle.get(id_=self.victim_vehicle_id)

    @property
    def world(self) -> World:
        """The World (continent) the player died on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the player died on."""
        return Zone.get(id_=self.zone_id)


class FacilityControl(Event):  # pylint: disable=too-many-instance-attributes
    """A facility has changed ownership.

    This is a world-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'FacilityControl'
    event_name = 'facility_control'
    event_type = 5

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
        """The Region (facility) that was captured."""
        from .. import namespace
        query = Query('map_region', namespace=namespace,
                      facility_id=self.facility_id)
        query.join('region', inject_at='region',
                   on='map_region_id', to='region_id')
        data = query.get(single=True)['region']
        return Region.get(id_=self.facility_id, data=data)

    @property
    def new_faction(self) -> Faction:
        """The Faction that captured the facility."""
        return Faction.get(id_=self.new_faction_id)

    @property
    def old_faction(self) -> Faction:
        """The Faction that lost the facility."""
        return Faction.get(id_=self.old_faction_id)

    @property
    def outfit(self) -> Outfit:
        """The Outfit that captured the facility."""
        return Outfit.get(id_=self.outfit_id)

    @property
    def world(self) -> World:
        """The World (server) the facility was captured on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) of the facility that was captured."""
        return Zone.get(id_=self.zone_id)


class GainExperience(Event):
    """A character has earned experience.

    This is a very common event that should be used with care. It can create a
    very large number of hits, even for a moderate list of tracked players.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'GainExperience'
    event_name = 'gain_experience'
    event_type = 6

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
        """The Character that gained experience."""
        return Character.get(id_=self.character_id)

    @property
    def experience(self) -> Experience:
        """The type of Experience the player got."""
        return Experience.get(id_=self.experience_id)

    @property
    def loadout(self) -> Loadout:
        """The Loadout of the player that gained experience."""
        return Loadout.get(id_=self.loadout_id)

    @property
    def world(self) -> World:
        """The World (continent) the player gained experience on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the player gained experience on."""
        return Zone.get(id_=self.zone_id)


class ItemAdded(Event):
    """A character has received an item.

    Sent when a player receives or unlocks an item, an implant drop or when
    cosmetics are granted to a player.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'ItemAdded'
    event_name = 'item_added'
    event_type = 7

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
        """The Character that gained the item."""
        return Character.get(id_=self.character_id)

    @property
    def item(self) -> Item:
        """The Item the character gained."""
        return Item.get(id_=self.item_id)

    @property
    def world(self) -> World:
        """The World (server) the character gained experience on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the character gained experience on."""
        return Zone.get(id_=self.zone_id)


class MetagameEvent(Event):  # pylint: disable=too-many-instance-attributes
    """An event or alert has started or ended.

    This is a world-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'MetagameEvent'
    event_name = 'metagame_event'
    event_type = 8

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
        """The type of Alert that started/ended."""
        return Alert.get(id_=self.metagame_event_id)

    @property
    def metagame_event_state(self) -> AlertState:
        """The AlertState of the alert."""
        return AlertState.get(id_=self.metagame_event_state)

    @property
    def world(self) -> World:
        """The World (server) the event started/ended on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the event started/ended on."""
        return Zone.get(id_=self.zone_id)


class PlayerFacilityCapture(Event):
    """A character has participated in capturing a facility.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'PlayerFacilityCapture'
    event_name = 'player_facility_capture'
    event_type = 9

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
        """The Character that captured the facility."""
        return Character.get(id_=self.character_id)

    @property
    def facility(self) -> Faction:
        """The Region the character captured."""
        return Region.get(id_=self.facility_id)

    @property
    def outfit(self) -> Outfit:
        """The Outfit that captured the facility."""
        return Outfit.get(id_=self.outfit_id)

    @property
    def world(self) -> World:
        """The World (server) the facility was captured on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) of the facility."""
        return Zone.get(id_=self.zone_id)


class PlayerFacilityDefend(Event):
    """A character has participated in defending a facility.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'PlayerFacilityDefend'
    event_name = 'player_facility_defend'
    event_type = 10

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
        """The Character that captured the facility."""
        return Character.get(id_=self.character_id)

    @property
    def facility(self) -> Region:
        """The Region the character captured."""
        return Region.get(id_=self.facility_id)

    @property
    def outfit(self) -> Outfit:
        """The Outfit that captured the facility."""
        return Outfit.get(id_=self.outfit_id)

    @property
    def world(self) -> World:
        """The World (server) the facility was captured on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) of the facility."""
        return Zone.get(id_=self.zone_id)


class PlayerLogin(Event):
    """A character has logged into their account.

    This event is both character-centric and world-centric.
    """

    # These attributes link the class to the event types and names
    census_name = 'PlayerLogin'
    event_name = 'player_login'
    event_type = 11

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.world_id = int(payload['world_id'])

    @property
    def character(self) -> Character:
        """The Character that logged in."""
        return Character.get(id_=self.character_id)

    @property
    def world(self) -> World:
        """The World (server) the character logged into."""
        return World.get(id_=self.world_id)


class PlayerLogout(Event):
    """A character has logged out of their account.

    This event is both character-centric and world-centric.
    """

    # These attributes link the class to the event types and names
    census_name = 'PlayerLogout'
    event_name = 'player_logout'
    event_type = 12

    def __init__(self, payload: dict) -> None:
        # Run the Event object's init method
        super().__init__(payload=payload)

        # Set attribute values
        self.character_id = int(payload['character_id'])
        self.world_id = int(payload['world_id'])

    @property
    def character(self) -> Character:
        """The Character that logged out."""
        return Character.get(id_=self.character_id)

    @property
    def world(self) -> World:
        """The World (server) the character logged out of."""
        return World.get(id_=self.world_id)


class SkillAdded(Event):
    """A character has unlocked or been granted a skill (certification).

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'SkillAdded'
    event_name = 'skill_added'
    event_type = 13

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
        """The Character that gained a skill."""
        return Character.get(id_=self.character_id)

    @property
    def skill(self) -> Skill:
        """The Skill gained by the character."""
        return Skill.get(id_=self.skill_id)

    @property
    def world(self) -> World:
        """The World (server) the character gained the skill on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the character gained the skill on."""
        return Zone.get(id_=self.zone_id)


class VehicleDestroy(Event):  # pylint: disable=too-many-instance-attributes
    """A vehicle has been destroyed in combat.

    This event will be sent regardless of whether the tracked player is the
    owner or the attacker.

    This is a character-centric event.
    """

    # These attributes link the class to the event types and names
    census_name = 'VehicleDestroy'
    event_name = 'vehicle_destroyed'
    event_type = 14

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
    def attacker(self) -> Optional[Character]:
        """The Character that destroyed the vehicle.

        Might be None.
        """
        return Character.get(id_=self.attacker_id)

    @property
    def attacker_loadout(self) -> Loadout:
        """The Loadout of the killing player."""
        return Loadout.get(id_=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self) -> Optional[Vehicle]:
        """The Vehicle of the killing player.

        Might be None."""
        return Vehicle.get(id_=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Weapon:
        """The Weapon of the killing player."""
        return Weapon.get(id_=self.attacker_weapon_id)

    @property
    def facility(self) -> Region:
        """The Region the vehicle was destroyed on."""
        return Region.get(id_=self.facility_id)

    @property
    def faction(self) -> Faction:
        """No information known."""
        return Faction.get(id_=self.faction_id)

    @property
    def victim(self) -> Character:
        """The Character that owned the destroyed vehicle."""
        return Character.get(id_=self.victim_id)

    @property
    def victim_vehicle(self) -> Vehicle:
        """The Vehicle type that was destroyed."""
        return Vehicle.get(id_=self.victim_vehicle_id)

    @property
    def world(self) -> World:
        """The World (server) the vehicle was destroyed on."""
        return World.get(id_=self.world_id)

    @property
    def zone(self) -> Zone:
        """The Zone (continent) the vehicle was destroyed on."""
        return Zone.get(id_=self.zone_id)
