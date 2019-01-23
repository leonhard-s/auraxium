"""Contains object representations of the PlanetSide 2 (PC) event types.

All classed defined herein are subclassed to the "Event" class. They are all
created by feeding them with the "payload" dictionary received by the event
streaming service.
"""

from datetime import datetime
from ....base_api import Query
from ...ps2 import (Achievement, Alert, AlertState, Character, Experience,
                    Faction, FireMode, Item, Loadout, Outfit, Region, Skill,
                    Vehicle, Weapon, World, Zone)


class AchievementEarned():
    """A character has earned an achievement (weapon medal or service ribbon).

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'AchievementEarned'

    def __init__(self, data):
        # Set attribute values
        self.achievment_id = data['achievement_id']
        self.character_id = data['character_id']

        self.timestamp = data['timestamp']
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def achievement(self):
        return Achievement.get(id=self.achievment_id)

    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class BattleRankUp():
    """A character has earned a battle rank (i.e. levelled up).

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'BattleRankUp'

    def __init__(self, data):
        # Set attribute values
        self.battle_rank = data['battle_rank']
        self.character_id = data['character_id']

        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class ContinentLock():
    """A continent has been locked (i.e. captured by a faction).

    (This is a world-centric event. Subscribe to one or more worlds (servers)
    to receive this event type.)

    """

    name = 'ContinentLock'

    def __init__(self, data):
        # Set attribute values

        self.metagame_event_id = data['metagame_event_id']
        self.metagame_event_type = data['event_type']
        self.population_nc = data['nc_population']
        self.population_tr = data['tr_population']
        self.population_vs = data['vs_population']
        self.previous_faction_id = data['previous_faction']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.triggering_faction_id = ['triggering_faction']
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def metagame_event(self):
        return Alert.get(id=self.metagame_event_id)

    @property
    def previous_faction(self):
        return Faction.get(id=self.previous_faction_id)

    @property
    def triggering_faction(self):
        return Faction.get(id=self.triggering_faction_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class ContinentUnlock():
    """A continent has been unlocked.

    (This is a world-centric event. Subscribe to one or more worlds (servers)
    to receive this event type.)

    """

    name = 'ContinentUnlock'

    def __init__(self, data):
        # Set attribute values

        self.metagame_event_id = data['metagame_event_id']
        self.metagame_event_type = data['event_type']
        self.population_nc = data['nc_population']
        self.population_tr = data['tr_population']
        self.population_vs = data['vs_population']
        self.previous_faction_id = data['previous_faction']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.triggering_faction_id = ['triggering_faction']
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def metagame_event(self):
        return Alert.get(id=self.metagame_event_id)

    @property
    def previous_faction(self):
        return Faction.get(id=self.previous_faction_id)

    @property
    def triggering_faction(self):
        return Faction.get(id=self.triggering_faction_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class Death():
    """A character has died or been killed.

    This event will be sent regardless of whether the tracked player is the
    victim or the killer.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'Death'

    def __init__(self, data):
        # Set attribute values
        self.attacker_id = data['attacker_character_id']
        self.attacker_fire_mode_id = data['attacker_fire_mode_id']
        self.attacker_loadout_id = data['attacker_loadout_id']
        self.attacker_vehicle_id = data['attacker_vehicle_id']
        self.attacker_weapon_id = data['attacker_weapon_id']

        self.is_critical = data.get('is_critical')
        self.is_headshot = data['is_headshot']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.victim_id = data['character_id']
        self.victim_loadout_id = data.get('loadout_id')
        self.victim_vehicle_id = data.get('vehicle_id')
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def attacker(self):
        return Character.get(id=self.attacker_id)

    @property
    def attacker_fire_mode(self):
        return FireMode.get(id=self.attacker_fire_mode_id)

    @property
    def attacker_loadout(self):
        return Loadout.get(id=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self):
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self):
        return Weapon.get(id=self.attacker_weapon_id)

    @property
    def victim(self):
        return Character.get(id=self.victim_id)

    @property
    def victim_loadout(self):
        return Loadout.get(id=self.victim_loadout_id)

    @property
    def victim_vehicle(self):
        return Vehicle.get(id=self.victim_vehicle_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class FacilityControl():
    """A facility has changed ownership.

    (This is a world-centric event. Subscribe to one or more worlds (servers)
    to receive this event type.)

    """

    name = 'FacilityControl'

    def __init__(self, data):
        # Set attribute values
        self.duration_held = data['duration_held']

        self.facility_id = data['facility_id']
        self.new_faction_id = data['new_faction_id']
        self.old_faction_id = data['old_faction_id']
        self.outfit_id = data['outfit_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def region(self):
        from . import namespace
        q = Query('map_region', namespace=namespace, facility_id=self.facility_id)
        q.join('region', inject_at='region', on='map_region_id', to='region_id')
        data = q.get(single=True)['region']
        return Region.get(id=self.facility_id, data=data)

    @property
    def new_faction(self):
        return Faction.get(id=self.new_faction_id)

    @property
    def old_faction(self):
        return Faction.get(id=self.old_faction_id)

    @property
    def outfit(self):
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class GainExperience():
    """A character has earned experience.

    This is a very common event that should be used with care. It can create a
    very large number of hits, even for a moderate list of tracked players.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'GainExperience'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']

        self.amount = data['amount']
        self.experience_id = data['experience_id']
        self.loadout_id = data['loadout_id']
        self.other_id = data['other_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def experience(self):
        return Experience.get(id=self.experience_id)

    @property
    def loadout(self):
        return Loadout.get(id=self.loadout_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class ItemAdded():
    """A character has received an item.

    Sent when a player receives or unlocks an item, an implant drop or when
    cosmetics are granted to a player.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'ItemAdded'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']
        self.context = data['context']

        self.item_count = data['item_count']
        self.item_id = data['item_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def item(self):
        return Item.get(id=self.item_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class MetagameEvent():
    """An event or alert has started or ended.

    (This is a world-centric event. Subscribe to one or more worlds (servers)
    to receive this event type.)

    """

    name = 'MetagameEvent'

    def __init__(self, data):
        # Set attribute values

        self.experience_bonus = data['experience_bonus']
        self.faction_nc = data['faction_nc']
        self.faction_tr = data['faction_tr']
        self.faction_vs = data['faction_vs']
        self.metagame_event_id = data['metagame_event_id']
        self._metagame_event_state = data['metagame_event_state']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def metagame_event(self):
        return Alert.get(id=self.metagame_event_id)

    @property
    def metagame_event_state(self):
        return AlertState.get(id=self._metagame_event_state)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class PlayerFacilityCapture():
    """A character has participated in capturing a facility.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'PlayerFacilityCapture'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']

        self.facility_id = data['facility_id']
        self.outfit_id = data['outfit_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def facility(self):
        return Region.get(id=self.facility_id)

    @property
    def outfit(self):
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class PlayerFacilityDefend():
    """A character has participated in defending a facility.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'PlayerFacilityDefend'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']

        self.facility_id = data['facility_id']
        self.outfit_id = data['outfit_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def facility(self):
        return Region.get(id=self.facility_id)

    @property
    def outfit(self):
        return Outfit.get(id=self.outfit_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class PlayerLogin():
    """A character has logged into their account.

    (This event is both character-centric and world-centric. It can be
    subscribed to using either the server or character ID.)

    """

    name = 'PlayerLogin'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']

        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def world(self):
        return World.get(id=self.world_id)


class PlayerLogout():
    """A character has logged out of their account.

    (This event is both character-centric and world-centric. It can be
    subscribed to using either the server or character ID.)

    """

    name = 'PlayerLogout'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']

        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def world(self):
        return World.get(id=self.world_id)


class SkillAdded():
    """A character has unlocked or been granted a skill (certification).

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'SkillAdded'

    def __init__(self, data):
        # Set attribute values
        self.character_id = data['character_id']
        self.skill_id = data['skill_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def character(self):
        return Character.get(id=self.character_id)

    @property
    def skill(self):
        return Skill.get(id=self.skill_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)


class VehicleDestroy():
    """A vehicle has been destroyed in combat.

    This event will be sent regardless of whether the tracked player is the
    owner or the attacker.

    (This is a character-centric event. Subscribe to one or more characters to
    receive this event type.)

    """

    name = 'VehicleDestroy'

    def __init__(self, data):
        # Set attribute values
        self.attacker_id = data['attacker_character_id']
        self.attacker_loadout_id = data['attacker_loadout_id']
        self.attacker_vehicle_id = data['attacker_vehicle_id']
        self.attacker_weapon_id = data['attacker_weapon_id']
        self.facility_id = data['facility_id']
        self.faction_id = data['faction_id']
        self.timestamp = datetime.utcfromtimestamp(int(data['timestamp']))
        self.victim_id = data['character_id']
        self.victim_vehicle_id = data['vehicle_id']
        self.world_id = data['world_id']
        self.zone_id = data['zone_id']

    # Define properties
    @property
    def attacker(self):
        return Character.get(id=self.attacker_id)

    @property
    def attacker_loadout(self):
        return Loadout.get(id=self.attacker_loadout_id)

    @property
    def attacker_vehicle(self):
        return Vehicle.get(id=self.attacker_vehicle_id)

    @property
    def attacker_weapon(self):
        return Weapon.get(id=self.attacker_weapon_id)

    @property
    def facility(self):
        return Region.get(id=self.facility_id)

    @property
    def faction(self):
        return Faction.get(id=self.faction_id)

    @property
    def victim(self):
        return Character.get(id=self.victim_id)

    @property
    def victim_vehicle(self):
        return Vehicle.get(id=self.victim_vehicle_id)

    @property
    def world(self):
        return World.get(id=self.world_id)

    @property
    def zone(self):
        return Zone.get(id=self.zone_id)
