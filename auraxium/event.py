"""Event definitions and utilities for the websocket event stream.

This mostly defines events, lists event types and defines the event
trigger system.

"""

import asyncio
import datetime
import enum
import json
import logging
import warnings
from typing import (Awaitable, Callable, Dict, Iterable, List, Optional, Set,
                    TYPE_CHECKING, Union)

from .types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .ps2 import Character, World

__all__ = [
    'ESS_ENDPOINT',
    'Event',
    'EventType',
    'Trigger'
]

# The websocket endpoint to connect to
ESS_ENDPOINT = 'wss://push.planetside2.com/streaming'
log = logging.getLogger('auraxium.ess')


class EventType(enum.IntEnum):
    """A type of event returned by the websocket."""

    # NOTE: IDs 1 through 19 are reserved for character-centric events,
    # IDs 20 through 29 are both character-centric and world-centric, and
    # IDs 30 and up are reserved for world-centric events.

    #: Fall-back value for unknown event types.
    UNKNOWN = 0

    # Character-centric events

    #: A character has earned a new achievement (medal or service ribbon).
    ACHIEVEMENT_EARNED = 1
    #: A character has achieved a new battle rank.
    BATTLE_RANK_UP = 2
    #: A character has been killed.
    DEATH = 3
    #: A character has been granted a new item.
    ITEM_ADDED = 4
    #: A character has been granted a new skill (certification/ASP skill).
    SKILL_ADDED = 5
    #: A character's vehicle has been destroyed.
    VEHICLE_DESTROY = 6
    #: A character has received an experience tick. The field ``other_id`` may
    # may refer to another player, vehicle, or entity.
    # Note that this is a very common event that can break your app if used on
    # large character groups.
    # Use :meth:`EventType.filter_experience()` to filter by experience ID.
    GAIN_EXPERIENCE = 7
    #: A character has participated in the capture of a facility.
    PLAYER_FACILITY_CAPTURE = 8
    #: A character has participated in the defence of a facility.
    PLAYER_FACILITY_DEFEND = 9

    # Character-centric and world-centric events

    #: A character has logged in.
    PLAYER_LOGIN = 20
    #: A character has logged out.
    PLAYER_LOGOUT = 21

    # World-centric events

    #: A continent has been locked.
    CONTINENT_LOCK = 30
    #: A continent has been unlocked. Note that this event is not working as of
    # July 2020.
    CONTINENT_UNLOCK = 31
    #: A facility has changed ownership (i.e. being captured).
    FACILITY_CONTROL = 32
    #: An alert has started or ended.
    METAGAME_EVENT = 33

    @classmethod
    def from_event_name(cls, event_name: str) -> 'EventType':
        """Return the appropriate enum value for the given name.

        The event name is case-insensitive here, not not in general.

        Returns:
            The event type for the given event payload, or
            :attr:`EventType.UNKNOWN`.

        """
        conversion_dict: Dict[str, int] = {
            'AchievementEarned': 1,
            'BattleRankUp': 2,
            'Death': 3,
            'ItemAdded': 4,
            'SkillAdded': 5,
            'VehicleDestroy': 6,
            'GainExperience': 7,
            'PlayerFacilityCapture': 8,
            'PlayerFacilityDefend': 9,
            'PlayerLogin': 20,
            'PlayerLogout': 21,
            'ContinentLock': 30,
            'ContinentUnlock': 31,
            'FacilityControl': 32,
            'MetagameEvent': 33}
        try:
            return cls(conversion_dict[event_name])
        except KeyError:
            # Fall-back for case-insensitive event names
            for name, id_ in conversion_dict.items():
                if name.lower() == event_name.lower():
                    return cls(id_)
            return cls(0)

    @classmethod
    def filter_experience(cls, experience_id: int) -> str:
        """Return a dynamic event matching events by experience ID.

        This works like :attr:`EventType.GAIN_EXPERIENCE`, but allows
        subscribing to only the experience IDs you are interested in.

        This reduces the bandwidth requirements as the number of
        GAIN_EXPERIENCE events can be excessively high for large groups
        of players.

        This returns a string that can be passed to both
        :meth:`Client.trigger()` and the :class:`Trigger` class's
        initialiser in place of the enum value itself.

        Arguments:
            experience_id: The experience ID to filter by.

        Returns:
            The event name filtering for the given experience ID.

        """
        event_name = cls.GAIN_EXPERIENCE.to_event_name()
        return f'{event_name}_experience_id_{experience_id}'

    @classmethod
    def from_payload(cls, payload: CensusData) -> 'EventType':
        """Return the appropriate enum value for the event.

        Returns:
            The event type for the given event payload, or
            :attr:`EventType.UNKNOWN`.

        """
        event_name = payload.get('event_name', 'NULL')
        return cls.from_event_name(event_name)

    def to_event_name(self) -> str:
        """Return the event name for the given enum value.

        This is mostly to dynamically subscribe to events.

        Raises:
            ValueError: Raised when calling this method on
                :attr:`EventType.UNKNOWN`.

        Returns:
            The string representing this event.

        """
        conversion_dict: Dict[int, str] = {
            1: 'AchievementEarned',
            2: 'BattleRankUp',
            3: 'Death',
            4: 'ItemAdded',
            5: 'SkillAdded',
            6: 'VehicleDestroy',
            7: 'GainExperience',
            8: 'PlayerFacilityCapture',
            9: 'PlayerFacilityDefend',
            20: 'PlayerLogin',
            21: 'PlayerLogout',
            30: 'ContinentLock',
            31: 'ContinentUnlock',
            32: 'FacilityControl',
            33: 'MetagameEvent'}
        try:
            return conversion_dict[self.value]
        except KeyError as err:
            raise ValueError(
                'Cannot convert EventType.UNKNOWN to event name') from err


class Event:
    """An event returned via the ESS websocket connection.

    The raw response returned through the API is accessible through the
    :attr:`payload` attribute.

    """

    def __init__(self, payload: CensusData) -> None:
        self.timestamp = datetime.datetime.utcfromtimestamp(
            int(payload['timestamp']))
        self.payload = payload

    @property
    def age(self) -> float:
        """The age of the event in seconds."""
        now = datetime.datetime.now()
        return (self.timestamp - now).total_seconds()

    @property
    def type(self) -> EventType:
        """The type of event."""
        return EventType.from_payload(self.payload)


class Trigger:
    """An event trigger for the client's websocket connection.

    Event triggers encapsulate both the event type to trigger on, as
    well as the action to perform when the event is encountered.

    They are also used to dynamically generate the subscription payload
    required to inform the event streaming service of the event types
    the client wishes to receive.

    Note that some subscriptions are incompatible with each other and
    may require multiple clients to be stable.

    Attributes:
        action: The method or coroutine to run if the matching event is
            encountered.
        characters: A list of characters to filter the incoming events
            by. For some events, like :attr:`EventType.DEATH`, there
            are multiple character IDs involved that may match.
        conditions: Any number of variables or callables that must be
            True for the trigger to run. Note that these filters are
            checked for any matching events, so any callables must be
            synchronous and lightweight.
        events: A set of events that the trigger will listen for.
        last_run: A :class:`datetime.datetime` instance that will be set
            to the last time the trigger has run. This will be
            ``None`` until the first run of the trigger.
        name: The unique name of the trigger.
        single_shot: If True, the trigger will be automatically removed
            from the client when it fires once.
        worlds: A list of worlds to filter the incoming events by.

    """

    def __init__(self, event: Union[EventType, str],
                 *args: Union[EventType, str],
                 characters: Optional[
                     Union[Iterable['Character'], Iterable[int]]] = None,
                 worlds: Optional[
                     Union[Iterable['World'], Iterable[int]]] = None,
                 action: Optional[
                     Callable[[Event], Union[None, Awaitable[None]]]] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        self.action = action
        self.characters: List[int] = (
            [] if characters is None else [c if isinstance(c, int) else c.id
                                           for c in characters])
        self.conditions: List[Union[bool, Callable[[CensusData], bool]]] = []
        self.events: Set[Union[EventType, str]] = set((event, *args))
        self.last_run: Optional[datetime.datetime] = None
        self.name = name
        self.single_shot = single_shot
        self.worlds: List[int] = (
            [] if worlds is None else [w if isinstance(w, int) else w.id
                                       for w in worlds])

    def callback(self, func: Callable[[Event], None]) -> None:
        """Set the given function as the trigger action.

        The action may be a regular callable or a coroutine.
        Any callable that is a coroutine according to
        :meth:`asyncio.iscoroutinefunction()` will be awaited.

        This method can be used as a decorator.

        .. code-block:: python3

            my_trigger = Trigger('Death')
            @my_trigger.callback
            def pay_respect(event):
                char = event.payload['character_id']
                print('F ({char})')

        Arguments:
            func: The method or coroutine to call when the event
                trigger fires.

        """
        self.action = func

    def check(self, event: Event) -> bool:
        """Return whether the given trigger should fire.

        This only returns whether the trigger should fire, the trigger
        action will be scheduled separately, at which point
        :meth:`Trigger.run()` is called.

        Arguments:
            event: The payload to check.

        Returns:
            Whether this trigger should run for the given event.

        """
        if event.type not in self.events:
            return False
        payload = event.payload
        # Check character ID requirements
        if self.characters:
            char_id = int(payload.get('character_id', 0))
            other_id = int(payload.get('attacker_character_id', 0))
            if char_id not in self.characters or other_id in self.characters:
                return False
        # Check world ID requirements
        if self.worlds:
            if int(payload.get('world_id', 0)) not in self.worlds:
                return False
        # Check custom trigger conditions
        for condition in self.conditions:
            if callable(condition):
                if not condition(payload):
                    return False
            elif not condition:
                return False
        return True

    def generate_subscription(self) -> str:
        """Generate the appropriate subscription for this trigger."""
        json_data: Dict[str, Union[str, List[str]]] = {
            'action': 'subscribe',
            'eventNames': [e.to_event_name() if isinstance(e, EventType) else e
                           for e in self.events],
            'service': 'event'}
        if self.characters:
            json_data['characters'] = [str(c) for c in self.characters]
        else:
            json_data['characters'] = ['all']
        if self.worlds:
            json_data['worlds'] = [str(c) for c in self.worlds]
        else:
            json_data['characters'] = ['all']
        return json.dumps(json_data)

    async def run(self, event: Event) -> None:
        """Perform the action associated with this trigger.

        Arguments:
            event: The event to pass to the trigger action.

        """
        self.last_run = datetime.datetime.now()
        if self.action is None:
            warnings.warn(f'Trigger {self} run with no action specified')
            return
        if asyncio.iscoroutinefunction(self.action):
            await self.action(event)  # type: ignore
        else:
            self.action(event)
