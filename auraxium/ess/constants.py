"""Contains constants and Enums used by the ESS submodule."""

from enum import Enum


class EventType(Enum):
    """Enumerates all known types of events."""

    ACHIEVEMENT_EARNED = 0
    BATTLE_RANK_UP = 1
    CONTINENT_LOCK = 2
    CONTINENT_UNLOCK = 3
    DEATH = 4
    FACILITY_CONTROL = 5
    GAIN_EXPERIENCE = 6
    ITEM_ADDED = 7
    METAGAME_EVENT = 8
    PLAYER_FACILITY_CAPTURE = 9
    PLAYER_FACILITY_DEFEND = 10
    PLAYER_LOGIN = 11
    PLAYER_LOGOUT = 12
    SKILL_ADDED = 13
    VEHICLE_DESTROY = 14


class Centricity(Enum):
    """Enumerates the centricities event types can have.

    The centricity of an event type decides whether it can be filtered
    or subscribed to by that object type (you cannot subscribe
    to "MetagameEvent" using a list of characters, etc.).
    """

    CHARACTER = 0
    WORLD = 1
    CHARACTER_AND_WORLD = 2
