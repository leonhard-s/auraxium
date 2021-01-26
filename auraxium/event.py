"""Event definitions and utilities for the websocket event stream.

This mostly defines events, lists event types and defines the event
trigger system.

"""

import asyncio
import contextlib
import datetime
import enum
import json
import logging
import warnings
from typing import (Any, Awaitable, Callable, Coroutine, Dict, Iterable,
                    Iterator, List, Optional, Set, TYPE_CHECKING, Union)

import websockets

from .client import Client
from .types import CensusData
from .utils import expo_scaled

if TYPE_CHECKING:  # pragma: no cover
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .ps2 import Character, World

__all__ = [
    'ESS_ENDPOINT',
    'Event',
    'EventClient',
    'EventType',
    'Trigger'
]

# The websocket endpoint to connect to
ESS_ENDPOINT = 'wss://push.planetside2.com/streaming'
log = logging.getLogger('auraxium.ess')

# Pylance is more strict regarding typing of synchronous vs. asynchronous code
Callback = Callable[['Event'], Union[Coroutine[Any, Any, None], None]]


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

        The event name is case-insensitive here, but not in general.

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
        :meth:`EventClient.trigger()` and the :class:`Trigger` class's
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
        self.timestamp: datetime.datetime = datetime.datetime.utcfromtimestamp(
            int(payload['timestamp']))
        self.payload: CensusData = payload

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
                 conditions: Optional[
                     List[Union[bool, Callable[[CensusData], bool]]]] = None,
                 action: Optional[
                     Callable[[Event], Union[None, Awaitable[None]]]] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        self.action = action
        self.characters: List[int] = (
            [] if characters is None else [c if isinstance(c, int) else c.id
                                           for c in characters])
        self.conditions: List[Union[bool, Callable[[CensusData], bool]]] = (
            [] if conditions is None else conditions)
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
        if (event.type not in self.events
                and event.type.to_event_name() not in self.events):
            # Extra check for the dynamically generated experience ID events
            if event.type == EventType.GAIN_EXPERIENCE:
                id_ = int(event.payload['experience_id'])
                for event_name in self.events:
                    if event_name == EventType.filter_experience(id_):
                        break
                else:
                    return False  # Dynamic event but non-matching ID
            else:
                return False
        payload = event.payload
        # Check character ID requirements
        if self.characters:
            char_id = int(payload.get('character_id', 0))
            other_id = int(payload.get('attacker_character_id', 0))
            if not (char_id in self.characters or other_id in self.characters):
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
            json_data['worlds'] = ['all']
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


class EventClient(Client):
    """Advanced client with event streaming capability.

    This subclass of :class:`Client` extends the interface to also
    provide access to the websocket endpoint at
    ``wss://push.planetside2.com/streaming``.

    To use the websocket endpoint, you have to define a
    :class:`Trigger` and register it using the
    :meth:`EventClient.add_trigger()` method. This will automatically
    open a websocket connection is there is not already one running.
    Likewise, removing all event triggers from the client will cause
    the underlying websocket connection to close.

    Refer to the :class:`Trigger` class's documentation for details on
    how to use triggers and respond to events.

    Attributes:
        triggers: The list of :class:`Triggers <Trigger>` registered
            for the client.
        websocket: The websocket client used for the real-time event
            stream. This will be automatically opened and closed by the
            client as event triggers are added and removed.

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.triggers: List[Trigger] = []
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._connect_lock = asyncio.Lock()
        self._connected: bool = False
        # NOTE: This utility returns a factory, hence the trailing parentheses
        self._reconnect_backoff = self._reset_backoff()
        self._send_queue: List[str] = []

    def add_trigger(self, trigger: Trigger) -> None:
        """Add a new event trigger to the client.

        If there is currently no active websocket connection to the
        event streaming service, one will be created for this trigger.

        .. note::
            As this is a synchronous method, the websocket will not be
            active by the time this method returns.
            Use :meth:`EventClient.wait_ready()` to wait for the
            websocket being ready.

        Arguments:
            trigger: The trigger to add.

        """
        log.debug('Adding trigger %s', trigger)
        self.triggers.append(trigger)
        subscription = trigger.generate_subscription()
        self._send_queue.append(subscription)
        # Only queue the connect() method if it is not already running
        if self.websocket is None and not self._connect_lock.locked():
            log.debug('Websocket not connected, scheduling connection')
            self.loop.create_task(self.connect())

    def find_trigger(self, name: str) -> Trigger:
        """Retrieve a registered event trigger by name.

        If the trigger cannot be found, a :class:`KeyError` is raised.

        Arguments:
            name: [description]

        Raises:
            KeyError: Raised if no trigger with the given name is
                registered for the client.

        """
        for trigger in self.triggers:
            if trigger.name == name:
                return trigger
        raise KeyError(f'No trigger with name "{name}" found')

    def remove_trigger(self, trigger: Union[Trigger, str], *,
                       keep_websocket_alive: bool = False) -> None:
        """Remove an existing event trigger.

        You can either provide the trigger instance to remove, or
        specify the name of the trigger instead.

        By default, the underlying websocket connection will be closed
        if this was the only trigger registered. Use the
        ``keep_websocket_alive`` flag to prevent this.

        Arguments:
            trigger: The trigger to remove, or its unique name.
            keep_websocket_alive (optional): If True, the websocket
                connection will be kept open even if the client has
                zero triggers remaining. Defaults to ``False``.

        Raises:
            KeyError: Raised if a trigger name was passed and no
                trigger of this name exists for the client.
            ValueError: Raised if no trigger of the given name is
                currently registered for this client.

        """
        if not isinstance(trigger, Trigger):
            trigger = self.find_trigger(trigger)
        log.debug('Removing trigger %s', trigger)
        try:
            self.triggers.remove(trigger)
        except ValueError as err:
            raise RuntimeError('The given trigger is not registered for '
                               'this client') from err
        # If this was the only trigger registered, close the websocket
        if not keep_websocket_alive and not self.triggers:
            log.info('All triggers have been removed, closing websocket')
            self.loop.create_task(self.close())

    async def close(self) -> None:
        """Shut down the client.

        This will close the websocket connection and end any ongoing
        HTTP sessions used for requests to the REST API.

        Call this to clean up before the client object is destroyed.

        """
        await self.disconnect()
        await super().close()

    async def connect(self) -> None:
        """Connect to the websocket endpoint and process responses.

        This will continuously loop until :meth:`EventClient.close()`
        is called.
        If the websocket connection encounters and error, it will be
        automatically restarted.

        Add payloads to :attr`EventClient._send_queue` to schedule
        their transmission.

        Any event payloads received will be passed to
        :meth:`EventClient.dispatch()` for filtering and event
        dispatch.

        """
        # NOTE: When multiple triggers are added to the bot without an active
        # websocket connection, this function may be scheduled multiple times.
        if self._connect_lock.locked():
            log.debug('Websocket already running')
            return
        await self._connect_lock.acquire()

        log.info('Connecting to websocket endpoint...')
        url = f'{ESS_ENDPOINT}?environment=ps2&service-id={self.service_id}'
        async with websockets.connect(url) as websocket:
            self.websocket = websocket
            log.info(
                'Connected to %s?environment=ps2&service-id=XXX', ESS_ENDPOINT)
            self._connected = True

            # Reset the backoff generator as the connection attempt was
            # successful
            self._reconnect_backoff = self._reset_backoff()

            # Keep processing websocket events until the connection dies or is
            # closed by the user or trigger system.
            while self._connect_lock.locked():
                try:
                    await self._handle_websocket()
                except websockets.exceptions.ConnectionClosed as err:
                    log.info('Websocket connection closed (%d, %s)',
                             err.code, err.reason)  # type: ignore
                    await self.disconnect()
                    # NOTE: This will increment the reconnect delay each time,
                    # until one connection attempt is successful.
                    delay = next(self._reconnect_backoff)
                    log.info(
                        'Next reconnection attempt in %.2f seconds', delay)
                    await asyncio.sleep(delay)
                    log.info('Attempting to reconnect...')
                    self.loop.create_task(self.connect())

    async def disconnect(self) -> None:
        """Disconnect the websocket.

        Unlike :meth:`EventClient.close()`, this does not affect the
        HTTP session used by regular REST requests.

        """
        if self.websocket is None:
            return
        log.info('Closing websocket connection')
        if self.websocket.open:
            await self.websocket.close()
        with contextlib.suppress(RuntimeError):
            self._connect_lock.release()
        self.websocket = None
        self._connected = False

    def dispatch(self, event: Event) -> None:
        """Dispatch an event to the appropriate event triggers.

        This goes through the list of triggers registered for this
        client and checks if the passed event matches the trigger's
        requirements using :meth:`Trigger.check()`.

        The call-backs for the matching triggers will be scheduled for
        execution in the current event loop using
        :meth:`asyncio.AbstractEventLoop.create_task()`.

        If a trigger's :attr:`Trigger.single_shot` attribute is set to
        True, the trigger will be removed from the client as soon as
        its call-back has been scheduled for execution. This means that
        when the action associated with a single-shot trigger runs, the
        associated trigger will no longer be registered for the client.

        Arguments:
            event: An event received through the event stream.

        """
        # Check for appropriate triggers
        for trigger in self.triggers:
            log.debug('Checking trigger %s', trigger)
            if trigger.check(event):
                log.debug('Scheduling trigger %s', trigger)
                self.loop.create_task(trigger.run(event))
                # Single-shot triggers self-unload as soon as their call-back
                # is scheduled
                if trigger.single_shot:
                    log.info('Removing single-shot trigger %s', trigger)
                    self.remove_trigger(trigger)

    async def _handle_websocket(self, timeout: float = 0.1) -> None:
        """Main loop handling the websocket connection.

        This method processes event payloads, adds automatic reconnect
        capabilities and sends messages added to
        :attr:`EventClient._send_queue`.
        """
        if self.websocket is None:
            return
        try:
            response = str(await asyncio.wait_for(
                self.websocket.recv(), timeout=timeout))
        except asyncio.TimeoutError:
            # NOTE: This inner timeout try block is used to ensure
            # the websocket will regularly check for messages in
            # the client's _send_queue even when no messages are
            # being received.
            # Without this, awaiting self.websocket.recv() would
            # block events from being sent if no responses are
            # received.
            pass
        else:
            log.debug('Received response: %s', response)
            self._process_payload(response)
        finally:
            if self._send_queue:
                msg = self._send_queue.pop(0)
                log.info('Sending message: %s', msg)
                await self.websocket.send(msg)

    def trigger(self, event: Union[str, EventType],
                *args: Union[str, EventType], name: Optional[str] = None,
                **kwargs: Any) -> Callable[[Callback], None]:
        """Create and add a trigger for the given action.

        If no name is specified, the call-back function's name will be
        used as the trigger name.

        Keep in mind that a trigger's name must be unique. A
        :class:`KeyError` will be raised if a trigger with this name
        already exists.

        Arguments:
            event: The event to trigger on.
            *args: Additional events that also trigger the action.
            name (optional): The name to assign to the trigger. If not
                specified, the call-back function's name will be used.
                Defaults to ``None``.

        Raises:
            KeyError: Raised if a trigger with the given name already
                exists.

        """
        trigger = Trigger(event, *args, name=name, **kwargs)

        def wrapper(func: Callback) -> None:
            trigger.action = func
            # If the trigger name has not been specified, use the call-back
            # function's name instead
            if trigger.name is None:
                trigger.name = func.__name__
            # Ensure the trigger name is unique before adding the trigger
            if any(t.name == trigger.name for t in self.triggers):
                raise KeyError(f'The trigger "{trigger.name}" already exists')
            # If the name is unique, register the trigger to the client
            self.add_trigger(trigger)

        return wrapper

    def _process_payload(self, response: str) -> None:
        """Process a response payload received through the websocket.

        This method filters out any non-event messages (such as service
        messages, connection heartbeats or subscription echoes) before
        passing any event payloads on to :meth:`EventClient.dispatch()`.

        Arguments:
            response: The plain text response received through the ESS.

        """
        data: CensusData = json.loads(response)
        service = data.get('service')
        # Event messages
        if service == 'event':
            if data['type'] == 'serviceMessage':
                event = Event(data['payload'])
                log.debug('%s event received, dispatching...', event.type)
                self.dispatch(event)
            elif data['type'] == 'heartbeat':
                log.debug('Heartbeat received: %s', data)
        # Subscription echo
        elif 'subscription' in data:
            log.debug('Subscription echo: %s', data)
        # Service state
        elif data.get('type') == 'serviceStateChange':
            log.info('Service state change: %s', data)
        # Push service
        elif service == 'push':
            log.debug('Ignoring push message: %s', data)
        # Help message
        elif 'send this for help' in data:
            log.info('ESS welcome message: %s', data)
        # Other
        else:
            log.warning('Unhandled message: %s', data)

    @staticmethod
    def _reset_backoff() -> Iterator[float]:
        """Reset the reconnect backoff generator."""
        return expo_scaled(factor=0.1, max_=30.0)()

    async def wait_for(self, trigger: Trigger, *args: Trigger,
                       timeout: Optional[float] = None) -> Event:
        """Wait for one or more triggers to fire.

        This method will wait until any of the given triggers have
        fired, or until the timeout has been exceeded.

        By default, any triggers passed will be automatically removed
        once the first has been triggered, regardless of the triggers'
        :attr:`Trigger.single_shot` setting.

        Arguments:
            trigger: A trigger to wait for.
            *args: Additional triggers that will also resume execution.
            timeout (optional): The maximum number of seconds to wait
                for; never expires if set to ``None``. Defaults to
                ``None``.

        Raises:
            TimeoutError: Raised if the given timeout is exceeded.

        Returns:
            The first event matching the given trigger(s).

        """
        # The following asyncio Event will pause this method until the trigger
        # fires or expires. Think of it as an asynchronous flag.
        async_flag = asyncio.Event()
        # Used to store the event received
        received_event: Optional[Event] = None

        triggers: List[Trigger] = [trigger]
        triggers.extend(args)

        def callback(event: Event) -> None:
            # Store the received event
            nonlocal received_event
            received_event = event
            # Remove the triggers. This suppresses any ValueErrors raised if
            # the trigger that fired was set to single shot mode.
            for trig in triggers:
                # NOTE: Due to Client.dispatch method being a normal method and
                # not a coroutine, it will always remove the trigger itself
                # before this call-back has any chance to fire (even through
                # the call-back itself is synchronous, it is wrapped in the
                # asynchronous Trigger.run method, causing this delay).
                #
                # This means that by the time this code is executed, the
                # trigger will already be removed, meaning that the ValueError
                # will always be raised here and not in Client.dispatch.
                with contextlib.suppress(ValueError):
                    self.remove_trigger(trig)
            # Set the flag to resume execution of the wait_for_event method
            async_flag.set()

        for trig in triggers:
            trig.action = callback
            self.add_trigger(trig)

        # Wait for the triggers to fire, or for the timeout to expire
        if timeout is not None and timeout <= 0.0:
            timeout = None
        try:
            await asyncio.wait_for(async_flag.wait(), timeout=timeout)
        except asyncio.TimeoutError as err:
            raise TimeoutError from err

        assert received_event is not None
        return received_event

    async def wait_ready(self, interval: float = 0.05) -> None:
        """Wait for the websocket connection to be ready.

        This will return once the websocket connection is open and
        active. This condition will be checked regularly as set by the
        ``interval`` argument.

        If the websocket is already active at the time this method is
        called, this will return without delay.

        Arguments:
            interval (optional): The interval at which to check the
                websocket connection's status. Defaults to ``0.05``.

        """
        if self._connected:
            return
        while not self._connected:
            await asyncio.sleep(interval)
