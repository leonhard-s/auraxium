import asyncio
import datetime
import json
import warnings
from typing import (Awaitable, Callable, Dict, Iterable, List, Optional, Set,
                    TYPE_CHECKING, Union)

from ..models.events import Event

if TYPE_CHECKING:  # pragma: no cover
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from ..ps2 import Character, World


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
            by. For some events, like :class:`auraxium.event.Death`,
            there are multiple character IDs involved that may match.
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

    def __init__(self, event: Union[Event, str],
                 *args: Union[Event, str],
                 characters: Optional[
                     Union[Iterable['Character'], Iterable[int]]] = None,
                 worlds: Optional[
                     Union[Iterable['World'], Iterable[int]]] = None,
                 conditions: Optional[
                     List[Union[bool, Callable[[Event], bool]]]] = None,
                 action: Optional[
                     Callable[[Event], Union[None, Awaitable[None]]]] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        self.action = action
        self.characters: List[int] = (
            [] if characters is None else [c if isinstance(c, int) else c.id
                                           for c in characters])
        self.conditions: List[Union[bool, Callable[[Event], bool]]] = (
            [] if conditions is None else conditions)
        self.events: Set[Union[Event, str]] = set((event, *args))
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
                char = event.character_id
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
            event: The event to check.

        Returns:
            Whether this trigger should run for the given event.

        """
        if (event not in self.events
                and event.__class__.__name__ not in self.events):
            # Extra check for the dynamically generated experience ID events
            if event.__class__.__name__ == 'GainExperience':
                id_ = event.experience_id
                for event_name in self.events:
                    if event_name == Event.filter_experience(id_):
                        break
                else:
                    return False  # Dynamic event but non-matching ID
            else:
                return False
        # Check character ID requirements
        if self.characters:
            char_id = event.character_id
            other_id = event.attacker_character_id
            if not (char_id in self.characters or other_id in self.characters):
                return False
        # Check world ID requirements
        if self.worlds:
            if event.world_id not in self.worlds:
                return False
        # Check custom trigger conditions
        for condition in self.conditions:
            if callable(condition):
                if not condition(event):
                    return False
            elif not condition:
                return False
        return True

    def generate_subscription(self) -> str:
        """Generate the appropriate subscription for this trigger."""
        json_data: Dict[str, Union[str, List[str]]] = {
            'action': 'subscribe',
            'eventNames': [e.__class__.__name__ for e in self.events],
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
