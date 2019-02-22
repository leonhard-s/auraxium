import json
from typing import Callable, List, Optional

from .events import EventType, event_type_to_census
from .typing import CharacterOrID, WorldOrID
from ..object_models.ps2 import Character, World


class EventListener():
    def __init__(self, *args: EventType, function: Callable,
                 characters: Optional[List[CharacterOrID]] = [],
                 worlds: Optional[List[WorldOrID]] = []) -> None:

        # Raise an error if no arguments were provided
        if not args:
            raise TypeError('At least 1 event type must be provided')

        self.characters = characters
        self.events = list(args)
        self.function = function
        self.worlds = worlds

    def subscribe(self) -> str:
        """Subscribes to any events required by the event listener."""

        # Create lists of IDs
        if self.characters:
            characters = [c for c in self.characters if isinstance(c, int)]
            characters.extend([int(c.id) for c in self.characters if isinstance(c, Character)])
        else:
            characters = []

        if self.worlds:
            worlds = [w for w in self.worlds if isinstance(w, int)]
            worlds.extend([int(w.id) for w in self.worlds if isinstance(w, World)])
        else:
            worlds = []

        # Serialize the event types
        events = [event_type_to_census(e) for e in self.events]

        # Generate the dictionary
        data: dict = {'action': 'subscribe',
                      'eventNames': events,
                      'service': 'event'}

        if characters:
            data['characters'] = characters

        if worlds:
            data['worlds'] = worlds

        # Return the JSON-stringified data
        return json.dumps(data)

    def remove(self, client) -> None:
        """Removes the event listener and unsubscribes if possible."""

        raise NotImplementedError('NYI')
