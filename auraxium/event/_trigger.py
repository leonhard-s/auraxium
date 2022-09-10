import asyncio
import datetime
import json
import warnings
from typing import (Any, Callable, Coroutine, Dict, Iterable, List, Optional,
                    Set, Type, Union)

from ..errors import CensusError
from ..models import CharacterEvent, Event, GainExperience
from ..ps2 import Character, World

_EventType = Union[Type[Event], str]
_Condition = Union[Any, Callable[[Event], bool]]
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

    .. attribute:: action
       :type: collections.abc.Callable[[auraxium.event.Event], None] | collections.abc.Callable[[typing.Coroutine[None]], None]

       The method or coroutine to run if the matching event is
       encountered.

    .. attribute:: characters
       :type: list[int]

       A list of characters to filter the incoming events by. For some
       events, like :class:`auraxium.event.Death`, both the victim and
       killer can lead to a match.

    .. attribute:: conditions
       :type: list[collections.abc.Callable[[auraxium.event.Event], bool]]

       Any number of callables that must return true for the trigger to
       run. Note that these filters are checked for any matching
       event types. Any callables used must be synchronous.

    .. attribute:: events
       :type: set[typing.Type[auraxium.event.Event] | str]

       A set of events that the trigger will listen for.

    .. attribute:: last_run
       :type: datetime.datetime | None

       A :class:`datetime.datetime` instance that will be set to the
       last time the trigger has run. This will be :obj:`None` until
       the first run of te trigger.

    .. attribute:: name
       :type: str

       The unique name of the trigger.

    .. attribute:: single_shot
       :type: bool

       If True, the trigger will be automatically removed from the
       client when it first fires.

    .. attribute:: worlds
       :type: list[int]

       A list of worlds to filter the incoming events by.
    """

    def __init__(self, event: _EventType, *args: _EventType,
                 characters: Optional[_CharConstraint] = None,
                 worlds: Optional[_WorldConstraint] = None,
                 conditions: Optional[List[_Condition]] = None,
                 action: Optional[_Action] = None,
                 name: Optional[str] = None,
                 single_shot: bool = False) -> None:
        """Initialise a new trigger.

        .. seealso::

           :meth:`auraxium.event.EventClient.trigger` -- Decorator used
           to define a trigger around a given function.

        :param event: The event type to trigger on.
        :type event: typing.Type[Event] or str
        :param args: Additional events to trigger on.
        :type args: typing.Type[Event] or str
        :param characters: A list of character constraints for the
           trigger.
        :type characters: collections.abc.Iterable[
           auraxium.ps2.Character] or collections.abc.Iterable[int] or None
        :param worlds: A list of world constraints for the trigger.
        :type worlds: collections.abc.Iterable[auraxium.ps2.World] or collections.abc.Iterable[int] or None
        :param conditions: A list of callables that must be true for
           the trigger to run.
        :type conditions: list[collections.abc.Callable[[Event], bool]] or None
        :param action: The method or coroutine to run if a matching
           event is encountered.
        :type action: collections.abc.Callable[[Event], None] or collections.abc.Callable[[typing.Coroutine[None]], None]
        :param name: The unique name of the trigger.
        :type name: str or None
        :param bool single_shot: If true, trigger will be removed from
           any client when it first fires.
        """
        self.action: Optional[_Action] = action
        self.characters: List[int] = []
        if characters is not None:
            self.characters = [
                c if isinstance(c, int) else c.id for c in characters]
        self.conditions: List[Callable[[Event], bool]] = conditions or []
        self.events: Set[_EventType] = set((event, *args))
        self.last_run: Optional[datetime.datetime] = None
        self.name: Optional[str] = name
        self.single_shot: bool = single_shot
        self.worlds: List[int] = []
        if worlds is not None:
            self.worlds = [w if isinstance(w, int) else w.id for w in worlds]

    def callback(self, func: _Action) -> None:
        """Set the given function as the trigger action.

        The action may be a regular callable or a coroutine.
        Any callable that is a coroutine function according to
        :func:`asyncio.iscoroutinefunction` will be awaited.

        This method can be used as a decorator.

        .. code-block:: python3

           my_trigger = Trigger('Death')

           @my_trigger.callback
           def pay_respect(event):
               char = event.character_id
               print('F ({char})')

        :param func: The method or coroutine to call when the event
           trigger fires.
        :type func: collections.abc.Callable[[Event], None] or collections.abc.Callable[[typing.Coroutine[None]], None]
        """
        self.action = func

    def check(self, event: Event) -> bool:
        """Return whether the given trigger should fire.

        This only returns whether the trigger should fire, the trigger
        action will be scheduled separately, at which point
        :meth:`Trigger.run()` is called.

        :param Event event: The event to check.
        :return: Whether this trigger should run for the given event.
        """
        if (event.__class__ not in self.events
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
        if self.worlds and event.world_id not in self.worlds:
            return False
        # Check custom trigger conditions
        for condition in self.conditions:
            if callable(condition):
                if not condition(event):
                    return False
            elif not condition:
                return False
        return True

    def generate_subscription(self, logical_and: Optional[bool] = None) -> str:
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
        if logical_and is not None:
            json_data['logicalAndCharactersWithWorlds'] = (
                'true' if logical_and else 'false')
        # When subscribing to character-centric events using only a world ID,
        # set the "logicalAnd*" flag to avoid subscribing to all characters on
        # all continents (characters would default to "all" if not specified).
        elif (self.worlds and not self.characters
                and any((issubclass(e, CharacterEvent))  # type: ignore
                        for e in self.events)):
            json_data['logicalAndCharactersWithWorlds'] = 'true'
        return json.dumps(json_data)

    async def run(self, event: Event) -> None:
        """Perform the action associated with this trigger.

        :param Event event: The event to pass to the trigger action.
        """
        self.last_run = datetime.datetime.utcnow()
        if self.action is None:  # pragma: no cover
            warnings.warn(f'Trigger {self.name} run with no action specified')
            return
        try:
            ret = self.action(event)
            if asyncio.iscoroutinefunction(self.action):
                assert ret is not None
                await ret
        except CensusError as err:  # pragma: no cover
            warnings.warn(f'Trigger {self.name} callback cancelled: {err}')
