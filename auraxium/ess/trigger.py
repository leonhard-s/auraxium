import asyncio
import json
from typing import Any, Callable, Dict, Iterable, Optional, Set
from .event import Event


class Trigger():
    def __init__(self, event_name: str, *args: str,
                 character_ids: Iterable[int] = [],
                 world_ids: Iterable[int] = [],
                 single_shot=False) -> None:
        self.events: Set[str] = set((event_name, *args))
        self._callback: Optional[Callable[[Event], None]] = None
        self.character_ids: Set[int] = set(character_ids)
        self.world_ids: Set[int] = set(world_ids)
        self.single_shot = single_shot

    def evaluate(self, payload: Dict[str, str]) -> bool:
        """Return whether this trigger should fire or not."""
        # Check the event name
        if payload['event_name'] not in self.events:
            print('Trigger eval failed: non-matching event_name '
                  f'{payload["event_name"]}')
            return False
        # Check the character_id, if applicable
        if 'character_id' in payload.keys():
            if (self.character_ids
                    and int(payload['character_id']) not in self.character_ids
                    and int(payload.get('attacker_character_id', 0)) not
                    in self.character_ids):
                if 'all' in self.character_ids:
                    return True
                print('Trigger eval failed: non-maching character_id '
                      f'{payload["character_id"]}')
                return False
        # Check the world_id, if applicable
        if 'world_id' in payload.keys():
            if (self.world_ids
                    and int(payload['world_id']) not in self.world_ids):
                if 'all' in self.world_ids:
                    return True
                print('Trigger eval failed: non-maching world_id '
                      f'{payload["world_id"]}')
                return False
        # Success
        return True

    def generate_subscription(self) -> str:
        """Generate the appropriate subscription for this trigger."""
        json_data: Dict[str, Any] = {'action': 'subscribe',
                                     'eventNames': list(self.events),
                                     'service': 'event'}
        if self.character_ids:
            json_data['characters'] = [str(c) for c in self.character_ids]
        if self.world_ids:
            json_data['worlds'] = [str(c) for c in self.world_ids]
        return json.dumps(json_data)

    async def run(self, event: Event) -> None:
        """Runs the callback, if specified."""
        if self._callback is None:
            raise RuntimeError('No callback specified')
        # The callback must only be awaited if it is a coroutine
        if asyncio.iscoroutine(self._callback):
            await self._callback(event)
        else:
            self._callback(event)

    def set_callback(self, func: Callable[[Event], None]) -> None:
        """Decorator for defining a trigger's coroutine."""
        self._callback = func
