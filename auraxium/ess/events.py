"""Defines the base Event class and provides a number of helper
functions to convert event names to their type or generate the
appropriate event object.
"""

from datetime import datetime

from .constants import Centricity, EventType

# This list links the indices of the EventType enum imported above to strings, which are referred
# to as the event name in the rest of the module.
_STRINGS = ['achievement_earned', 'battle_rank_up', 'continent_lock', 'continent_unlock',
            'death', 'facility_control', 'gain_experience', 'item_added', 'metagame_event',
            'player_facility_capture', 'player_facility_defend', 'player_login',
            'player_logout', 'skill_added', 'vehicle_destroy']


class Event():  # pylint: disable=too-few-public-methods
    """Base class for all event objects used by the ESS.

    Event Objects contain common information like the time the event
    was received or the type of event, as well as a number of event
    type specific fields.

    Do not instantiate this class manually; use `get` factory method
    instead.

    Parameters
    ----------
    `payload`: The payload dictionary to populate the Event with.
    """


    def __init__(self, payload: dict) -> None:
        self.name = event_type_to_string(census_to_event_type(payload['event_name']))
        self.timestamp = datetime.utcfromtimestamp(int(payload['timestamp']))
        self.type = string_to_event_type(self.name)


def census_to_event_type(event_string: str) -> EventType:
    """Converts an census event string to an event type.

    Raises a ValueError if the string given does not match any event
    names.
    """

    _STRINGS = ['AchievementEarned', 'BattleRankUp', 'ContinentLock', 'ContinentUnlock', 'Death',
                'FacilityControl', 'GainExperience', 'ItemAdded', 'MetagameEvent',
                'PlayerFacilityCapture', 'PlayerFacilityDefend', 'PlayerLogin', 'PlayerLogout',
                'SkillAdded', 'VehicleDestroy']

    # If the string passed is not a known event name, raise an error
    if not event_string in _STRINGS:
        raise ValueError('Unknown event name: {}'.format(event_string))

    return EventType(_STRINGS.index(event_string))


def check_centricity(event_type: EventType, centricity: Centricity) -> bool:
    """Checks whether the given event type is of the given centricity.

    Useful for checking whether specifying a character or world list is
    sensible for a given event type.
    """

    # Get the string representation of the event to facilitate the list comparison
    event_name = event_type_to_string(event_type=event_type)

    # Hard-coded lists of the event type centricities
    CHARACTER_CENTRIC = ['achievement_earned', 'battle_rank_up', 'death', 'gain_experience',
                         'item_added', 'skill_added', 'player_facility_capture',
                         'player_facility_defend', 'player_login', 'player_logout',
                         'vehicle_destroy']
    WORLD_CENTRIC = ['continent_lock', 'continent_unlock', 'facility_control', 'metagame_event',
                     'player_login', 'player_logout']

    # Check centricity
    if centricity == Centricity.CHARACTER and event_name in CHARACTER_CENTRIC:
        return True
    if centricity == Centricity.WORLD and event_name in WORLD_CENTRIC:
        return True
    if (centricity == Centricity.CHARACTER_AND_WORLD and event_name in CHARACTER_CENTRIC
            and event_name in WORLD_CENTRIC):
        return True

    # If it's not True, it has to be False
    return False


def event_type_to_census(event_type: EventType) -> str:
    """Converts an event type into the census version of its string."""

    _STRINGS = ['AchievementEarned', 'BattleRankUp', 'ContinentLock', 'ContinentUnlock', 'Death',
                'FacilityControl', 'GainExperience', 'ItemAdded', 'MetagameEvent',
                'PlayerFacilityCapture', 'PlayerFacilityDefend', 'PlayerLogin', 'PlayerLogout',
                'SkillAdded', 'VehicleDestroy']

    return _STRINGS[event_type.value]


def event_type_to_string(event_type: EventType) -> str:
    """Converts an event type into its string representation.

    Returns the string corresponding to the EventType enum's value.
    """

    return _STRINGS[event_type.value]


def get_event(payload: dict) -> Event:  # pylint: disable=too-many-locals
    """Returns the corresponding event type for the given payload."""

    from .ps2 import (AchievementEarned, BattleRankUp, ContinentLock, ContinentUnlock, Death,
                      FacilityControl, GainExperience, ItemAdded, MetagameEvent,
                      PlayerFacilityCapture, PlayerFacilityDefend, PlayerLogin, PlayerLogout,
                      SkillAdded, VehicleDestroy)

    EVENT_TYPES = [AchievementEarned, BattleRankUp, ContinentLock, ContinentUnlock, Death,
                   FacilityControl, GainExperience, ItemAdded, MetagameEvent,
                   PlayerFacilityCapture, PlayerFacilityDefend, PlayerLogin, PlayerLogout,
                   SkillAdded, VehicleDestroy]

    return EVENT_TYPES[census_to_event_type(payload['event_name']).value](payload=payload)


def string_to_event_type(event_name: str) -> EventType:
    """Converts an event name to an event type.

    Attempts to retrieve the event type corresponding to the given
    string.

    Raises a ValueError if the string given does not match any event
    names.
    """

    # If the string passed is not a known event name, raise an error
    if not event_name in _STRINGS:
        raise ValueError('Unknown event name: {}'.format(event_name))

    return EventType(_STRINGS.index(event_name))
