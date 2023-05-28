"""Event definitions and utilities for the WebSocket event stream.

This module contains the custom :class:`EventClient` that adds support
for the real-time endpoint, defines the available event types, and
provides a trigger system used to respond to in-game events.
"""

from ._client import EventClient
from ._trigger import Trigger
from ..models import (AchievementAdded, BattleRankUp, Death, Event,
                      FacilityControl, GainExperience, ItemAdded,
                      MetagameEvent, PlayerFacilityCapture,
                      PlayerFacilityDefend, PlayerLogin, PlayerLogout,
                      SkillAdded, VehicleDestroy, ContinentLock)

__all__ = [
    'Event',
    'EventClient',
    'Trigger',

    # Event subclasses
    'AchievementAdded',
    'BattleRankUp',
    'ContinentLock',
    'Death',
    'FacilityControl',
    'GainExperience',
    'ItemAdded',
    'MetagameEvent',
    'PlayerFacilityCapture',
    'PlayerFacilityDefend',
    'PlayerLogin',
    'PlayerLogout',
    'SkillAdded',
    'VehicleDestroy'
]
