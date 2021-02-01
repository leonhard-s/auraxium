from __future__ import annotations

import datetime
from abc import abstractmethod
from typing import Literal, Dict, Any

from pydantic import Field

from auraxium.base import Ps2Data
from auraxium.event_util import EventType


class SubscriptionMessage(Ps2Data):
    subscription: Dict[str, Any]
    # subscription: create_model('Subscription',
    #                            eventNames=(List[str], ...),
    #                            logicalAndCharactersWithWorlds=(bool, ...),
    #                            worlds=(List[int], ...),
    #                            characterCount=(Optional[int]))


class PushMessage(Ps2Data):
    service: Literal['push']
    connected: bool  # not sure if this is required or not...


class EventMessage(Ps2Data):
    service: Literal['event']


class HelpMessage(Ps2Data):
    send_this_for_help: EventMessage = Field(..., alias='send this for help')


class HeartbeatMessage(EventMessage):
    type: Literal['heartbeat']


class ServiceStateChangedMessage(EventMessage):
    type: Literal['serviceStateChanged']
    detail: str
    online: bool


class Event(Ps2Data):
    timestamp: int
    type: 'EventType'
    world_id: int
    zone_id: int

    @classmethod
    def get_name(cls):
        return cls.__name__

    @property
    def age(self) -> float:
        """The age of the event in seconds."""
        now = datetime.datetime.utcnow()
        return (datetime.datetime.utcfromtimestamp(self.timestamp) - now).total_seconds()

    @property
    def type(self) -> EventType:
        return EventType.from_event_name(self.__class__.__name__)

    @property
    @abstractmethod
    def event_name(self):
        """Define the abstract property event_name for subclasses, allows a common getter for Event and EventType"""
        pass

    def get_event_name(self):
        return self.event_name
