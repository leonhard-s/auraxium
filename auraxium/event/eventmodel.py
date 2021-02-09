from __future__ import annotations

import datetime
import enum
from typing import Literal, Dict, Any

from pydantic import Field

from auraxium.base import Ps2Data

__all__ = [
    "Event",
    "EventMessage",
    "EventType",
    "HeartbeatMessage",
    "HelpMessage",
    "PushMessage",
    "ServiceStateChangedMessage",
    "SubscriptionMessage",
]


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
    type: EventType
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

    @classmethod
    def get_event_name(cls) -> str:
        return cls.get_name()


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
        event_name = cls.GAIN_EXPERIENCE.get_event_name()
        return f'{event_name}_experience_id_{experience_id}'

    # @classmethod
    # def from_payload(cls, payload: CensusData) -> 'EventType':
    #     """Return the appropriate enum value for the event.
    #
    #     Returns:
    #         The event type for the given event payload, or
    #         :attr:`EventType.UNKNOWN`.
    #
    #     """
    #     event_name = payload.get('event_name', 'NULL')
    #     return cls.from_event_name(event_name)

    def get_event_name(self) -> str:
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
