"""Contains object representations of the PlanetSide 2 event types.

All classed defined herein are subclassed to the "Event" class. They
are all created by feeding them with the "payload" dictionary received
by the event streaming service.
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
        """The Achievement the character has earned."""

    @property
    def character(self) -> Character:
        return Character.get(id=self.character_id)
        """The Character that earned the achievement."""

    @property
    def world_id(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the achievement was earned on."""

    @property
    def zone_id(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the achievement was earned on."""


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
        """The Character that earned a battle rank."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the battle rank was earned on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the battle rank was earned on."""


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
        """The Alert that locked the continent."""

    @property
    def previous_faction(self) -> Faction:
        return Faction.get(id=self.previous_faction_id)
        """The Faction that owned the continent until now."""

    @property
    def triggering_faction(self) -> Faction:
        return Faction.get(id=self.triggering_faction_id)
        """The Faction that captured the continent."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the continent was locked on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) that was locked."""


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
        """The Alert that unlocked the continent."""

    @property
    def previous_faction(self) -> Faction:
        return Faction.get(id=self.previous_faction_id)
        """No information known."""

    @property
    def triggering_faction(self) -> Faction:
        return Faction.get(id=self.triggering_faction_id)
        """No information known."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the continent was unlocked on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) that was unlocked."""


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
        """The Character that killed the victim."""

    @property
    def attacker_fire_mode(self) -> FireMode:
        return FireMode.get(id=self.attacker_fire_mode_id)
        """The FireMode used to kill the victim."""

    @property
    def attacker_loadout(self) -> Loadout:
        return Loadout.get(id=self.attacker_loadout_id)
        """The Loadout the killing player was using."""

    @property
    def attacker_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Weapon:
        return Weapon.get(id=self.attacker_weapon_id)

    @property
    def victim(self) -> Character:
        return Character.get(id=self.victim_id)
        """The Character that has died."""

    @property
    def victim_loadout(self) -> Loadout:
        return Loadout.get(id=self.victim_loadout_id)
        """The Loadout the victim was using."""

    @property
    def victim_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.victim_vehicle_id)

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (continent) the player died on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the player died on."""


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
        """The Region (facility) that was captured."""
        from .. import namespace
        q = Query('map_region', namespace=namespace, facility_id=self.facility_id)
        q.join('region', inject_at='region', on='map_region_id', to='region_id')
        data = q.get(single=True)['region']
        return Region.get(id=self.facility_id, data=data)

    @property
    def new_faction(self) -> Faction:
        return Faction.get(id=self.new_faction_id)
        """The Faction that captured the facility."""

    @property
    def old_faction(self) -> Faction:
        return Faction.get(id=self.old_faction_id)
        """The Faction that lost the facility."""

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)
        """The Outfit that captured the facility."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the facility was captured on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) of the facility that was captured."""


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
        """The Character that gained experience."""

    @property
    def experience(self) -> Experience:
        return Experience.get(id=self.experience_id)
        """The type of Experience the player got."""

    @property
    def loadout(self) -> Loadout:
        return Loadout.get(id=self.loadout_id)
        """The Loadout of the player that gained experience."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (continent) the player gained experience on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the player gained experience on."""


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
        """The Character that gained the item."""

    @property
    def item(self) -> Item:
        return Item.get(id=self.item_id)
        """The Item the character gained."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the character gained experience on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the character gained experience on."""


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
        """The type of Alert that started/ended."""

    @property
    def metagame_event_state(self) -> AlertState:
        return AlertState.get(id=self.metagame_event_state)
        """The AlertState of the alert."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the event started/ended on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the event started/ended on."""


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
        """The Character that captured the facility."""

    @property
    def facility(self) -> Faction:
        return Region.get(id=self.facility_id)
        """The Region the character captured."""

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)
        """The Outfit that captured the facility."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the facility was captured on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) of the facility."""


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
        """The Character that captured the facility."""

    @property
    def facility(self) -> Region:
        return Region.get(id=self.facility_id)
        """The Region the character captured."""

    @property
    def outfit(self) -> Outfit:
        return Outfit.get(id=self.outfit_id)
        """The Outfit that captured the facility."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the facility was captured on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) of the facility."""


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
        """The Character that logged in."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the character logged into."""


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
        """The Character that logged out."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the character logged out of."""


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
        """The Character that gained a skill."""

    @property
    def skill(self) -> Skill:
        return Skill.get(id=self.skill_id)
        """The Skill gained by the character."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the character gained the skill on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the character gained the skill on."""


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
        """The Loadout of the killing player."""

    @property
    def attacker_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self) -> Weapon:
        return Weapon.get(id=self.attacker_weapon_id)
        """The Weapon of the killing player."""

    @property
    def facility(self) -> Region:
        return Region.get(id=self.facility_id)
        """The Region the vehicle was destroyed on."""

    @property
    def faction(self) -> Faction:
        return Faction.get(id=self.faction_id)
        """No information known."""

    @property
    def victim(self) -> Character:
        return Character.get(id=self.victim_id)
        """The Character that owned the destroyed vehicle."""

    @property
    def victim_vehicle(self) -> Vehicle:
        return Vehicle.get(id=self.victim_vehicle_id)
        """The Vehicle type that was destroyed."""

    @property
    def world(self) -> World:
        return World.get(id=self.world_id)
        """The World (server) the vehicle was destroyed on."""

    @property
    def zone(self) -> Zone:
        return Zone.get(id=self.zone_id)
        """The Zone (continent) the vehicle was destroyed on."""
