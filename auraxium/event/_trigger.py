import asyncio
import datetime
import json
import warnings
from typing import (Any, Callable, Coroutine, Dict, Iterable, List, Optional,
                    Set, Type, Union)

from ..errors import MaintenanceError, CensusError
from ..models import Event, GainExperience
from ..ps2 import Character, World

_EventType = Union[Type[Event], str]
_Condition = Callable[[Event], bool]
_Action = Callable[[Event], Union[Coroutine[Any, Any, None], None]]
_CharConstraint = Union[Iterable[Character], Iterable[int]]
_WorldConstraint = Union[Iterable[World], Iterable[int]]


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

    def __init__(self, event: _EventType, *args: _EventType,
                 characters: Optional[_CharConstraint] = None,
                 worlds: Optional[_WorldConstraint] = None,
                 conditions: Optional[List[_Condition]] = None,
                 action: Optional[_Action] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        self.action = action
        self.characters: List[int] = []
        if characters is not None:
            self.characters = [
                c if isinstance(c, int) else c.id for c in characters]
        self.conditions: List[Callable[[Event], bool]] = conditions or []
        self.events: Set[_EventType] = set((event, *args))
        self.last_run: Optional[datetime.datetime] = None
        self.name = name
        self.single_shot = single_shot
        self.worlds: List[int] = []
        if worlds is not None:
            self.worlds = [w if isinstance(w, int) else w.id for w in worlds]

    def callback(self, func: _Action) -> None:
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
            if isinstance(event, GainExperience):
                id_ = event.experience_id
                for event_name in self.events:
                    if event_name == GainExperience.filter_experience(id_):
                        break
                else:
                    return False  # Dynamic event but non-matching ID
            else:
                return False
        # Check character ID requirements
        if self.characters:
            char_id = int(getattr(event, 'character_id', -1))
            other_id = int(getattr(event, 'attacker_character_id', -1))
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
            'eventNames': [e if isinstance(e, str) else e.__name__
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
            warnings.warn(f'Trigger {self.name} run with no action specified')
            return
        try:
            ret = self.action(event)
            if asyncio.iscoroutinefunction(self.action):
                assert ret is not None
                await ret
        except (MaintenanceError, CensusError) as err:
            warnings.warn(f'Trigger {self.name} callback cancelled: {err}')
