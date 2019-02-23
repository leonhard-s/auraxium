"""Defines the base Event class and provides a number of helper
functions to convert event names to their type or generate the
appropriate event object.
"""

from datetime import datetime
from typing import List, Type

from .constants import Centricity, EventType
from .exceptions import EventTypeAmbiguityError, UnknownEventTypeError


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

    # These attributes are never used; they are just there to help the linting and make it
    # immediately obvious that something went wrong when debugging.
    census_name = 'NoEvent'
    event_name = 'no_event'
    event_type = -1

    def __init__(self, payload: dict) -> None:
        # While this method is overwritten by the subclasses, it is run manually before their own
        # initialization code runs.
        self.name: str = type_to_arx_name(census_name_to_type(census_name=payload['event_name']))
        self.timestamp = datetime.utcfromtimestamp(int(payload['timestamp']))
        self.type: EventType = arx_name_to_type(arx_name=self.name)

    @staticmethod
    def get(payload: dict) -> 'Event':
        """Factory method for Event objects.

        Returns the appropriate subclass of Event for the payload
        provided.

        Parameters
        ----------
        `payload`: The payload dictionary to retrieve the Event for.

        Raises
        ------
        `UnknownEventTypeError`: Raised when an event of unknown type
        is received.
        """

        # Try to find a matching subclass
        class_list: List[Type[Event]] = [cls for cls in Event.__subclasses__()
                                         if cls.census_name == payload['event_name']]

        # If no class matches, raise an error
        if not class_list:
            raise UnknownEventTypeError('Unknown event type: {}'.format(
                payload['event_name']))

        # If more than one class matches, we also have a problem.
        if len(class_list) > 1:
            raise EventTypeAmbiguityError('Multiple events referencing event name: {}'.format(
                payload['event_name']))

        # Get the event object
        event_type: Type[Event] = class_list[0]

        return event_type(payload)


def arx_name_to_type(arx_name: str) -> EventType:
    """Converts an event name to the corresponding event type.

    Raises
    ------
    `UnknownEventTypeError`: Raised when no event type matches the
    auraxium event name passed."""

    # Create a list of all matching event types
    type_list = [cls.event_type for cls in Event.__subclasses__() if cls.event_name == arx_name]

    # If the list is empty, raise an error
    if not type_list:
        raise UnknownEventTypeError('No event type registered for string: {}'.format(arx_name))

    # Do not bother checking for ambiguity
    return EventType(type_list[0])


def census_name_to_type(census_name: str) -> EventType:
    """Converts an census event string to an event type.

    Raises
    ------
    `UnknownEventTypeError`: Raised when the census name given does not match any
    event names.
    """

    # Create a list of all matching event types
    type_list = [cls.event_type for cls in Event.__subclasses__()
                 if cls.census_name == census_name]

    # If no matches were found, raise an error
    if not type_list:
        raise UnknownEventTypeError('Unknown census event name: {}'.format(census_name))

    # Do not bother checking for duplicates
    return EventType(type_list[0])


def check_centricity(event_type: EventType, centricity: Centricity) -> bool:
    """Checks whether the event type specified has the given centricity.

        At least one argument must be provided.

        Parameters
        ----------
        `centricity`: The centricity to check for.

        Returns
        -------
        `bool`: "True" if the centricity passed is valid for the event
        type, otherwise returns "False".
        """

    # Get the string representation of the event to facilitate the list comparison
    event_name = type_to_arx_name(event_type=event_type)

    # Hard-coded lists of the event type centricities
    character_centric = ['achievement_earned', 'battle_rank_up', 'death', 'gain_experience',
                         'item_added', 'skill_added', 'player_facility_capture',
                         'player_facility_defend', 'player_login', 'player_logout',
                         'vehicle_destroy']
    world_centric = ['continent_lock', 'continent_unlock', 'facility_control',
                     'metagame_event', 'player_login', 'player_logout']

    # Check centricity
    if (centricity in [Centricity.CHARACTER, Centricity.CHARACTER_AND_WORLD]
            and event_name not in character_centric):
        return False
    if (centricity in [Centricity.WORLD, Centricity.CHARACTER_AND_WORLD]
            and event_name not in world_centric):
        return False

    return True


def type_to_arx_name(event_type: EventType) -> str:
    """Returns the auraxium event name for this event type."""
    name_list = [cls.event_name for cls in Event.__subclasses__() if cls.event_type ==
                 event_type.value]

    # Raise an error if no match could be found
    if not name_list:
        raise UnknownEventTypeError(event_type)

    # Do not bother checking for ambiguity
    return str(name_list[0])


def type_to_census_name(event_type: EventType) -> str:
    """Returns the census event name for this event type."""
    name_list = [cls.census_name for cls in Event.__subclasses__() if cls.event_type ==
                 event_type.value]

    # Raise an error if no match could be found
    if not name_list:
        raise UnknownEventTypeError(event_type)

    # Do not bother checking for ambiguity
    return str(name_list[0])
