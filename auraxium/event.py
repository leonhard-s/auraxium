"""Event system used for the real-time websocket stream."""

import asyncio
import datetime
import enum
import json
import logging
import warnings
from typing import (Callable, Dict, Iterable, List, Optional, Set,
                    TYPE_CHECKING, Union)

from .types import CensusData

if TYPE_CHECKING:
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

    UNKNOWN = 0

    # Character-centric events
    ACHIEVEMENT_EARNED = 1
    BATTLE_RANK_UP = 2
    DEATH = 3
    ITEM_ADDED = 4
    SKILL_ADDED = 5
    VEHICLE_DESTROY = 6
    GAIN_EXPERIENCE = 7
    PLAYER_FACILITY_CAPTURE = 8
    PLAYER_FACILITY_DEFEND = 9

    # Character-centric and world-centric events
    PLAYER_LOGIN = 20
    PLAYER_LOGOUT = 21

    # World-centric events
    CONTINENT_LOCK = 30
    CONTINENT_UNLOCK = 31
    FACILITY_CONTROL = 32
    METAGAME_EVENT = 33

    @classmethod
    def from_event_name(cls, event_name: str) -> 'EventType':
        """Return the appropriate enum value for the given name.

        Returns:
            The event type for the given event payload, or
            ``EventType.UNKNOWN``.
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
        return cls(conversion_dict.get(event_name, 0))

    @classmethod
    def from_payload(cls, payload: CensusData) -> 'EventType':
        """Return the appropriate enum value for the event.

        Returns:
            The event type for the given event payload, or
            ``EventType.UNKNOWN``.
        """
        event_name = payload.get('event_name', 'NULL')
        return cls.from_event_name(event_name)

    def to_event_name(self) -> str:
        """Return the event name for the given enum value.

        This is mostly to dynamically subscribe to events.

        Raises:
            ValueError: Raised when calling this method on
                ``EventType.UNKNOWN``.

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
    """An event returned via the ESS websocket connection."""

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
    """An event trigger for the websocket connection.

    Event triggers encapsulate both the event type to trigger on, as
    well as the action to perform when the event is encountered.

    They are also used to dynamically generate the subscription payload
    required.

    Note that some subscriptions are incompatible with each other and
    may require multiple clients to be stable.
    """

    def __init__(self, event: Union[EventType, str],
                 *args: Union[EventType, str],
                 characters: Optional[
                     Union[Iterable['Character'], Iterable[int]]] = None,
                 worlds: Optional[
                     Union[Iterable['World'], Iterable[int]]] = None,
                 action: Optional[Callable[[Event], None]] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        self.action = action
        self.characters: List[int] = (
            [] if characters is None else [c if isinstance(c, int) else c.id
                                           for c in characters])
        self.events: Set[EventType] = {
            EventType.from_event_name(e) if isinstance(e, str) else e
            for e in (event, *args)}
        self.filters: List[Callable[[CensusData], bool]] = []
        self.last_run: Optional[datetime.datetime] = None
        self.name = name or 'Anonymous Trigger'
        self.single_shot = single_shot
        self.worlds: List[int] = (
            [] if worlds is None else [w if isinstance(w, int) else w.id
                                       for w in worlds])

    def callback(self, func: Callable[[Event], None]) -> None:
        """Set the given function as the trigger action.

        The action may be a regular callable or a coroutine.
        Any callable that is a corutine according to
        :meth:`asyncio.iscoroutine()` will be awaited.

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
        callback will be scheduled separately, at which point
        :meth:`Trigger.run()` is called.

        Arguments:
            event: The paylaod to check.

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
            if not char_id in self.characters or other_id in self.characters:
                return False
        # Check world ID requirements
        if self.worlds:
            if not int(payload.get('world_id', 0)) in self.worlds:
                return False
        # Check custom trigger filters
        return all(f(event) for f in self.filters)

    def generate_subscription(self) -> str:
        """Generate the appropriate subscription for this trigger."""
        json_data: Dict[str, str] = {
            'action': 'subscribe',
            'eventNames': [e.to_event_name() for e in self.events],
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

        This coroutine can be anything.

        Arguments:
            event: The event to pass to the trigger action.

        """
        self.last_run = datetime.datetime.now()
        if self.action is None:
            warnings.warn(f'Trigger {self} run with no action specified')
            return
        if asyncio.iscoroutine(self.action):
            await self.action(event)
        else:
            self.action(event)
