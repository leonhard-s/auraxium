"""Event definitions and utilities for the websocket event stream.

This mostly defines events, lists event types and defines the event
trigger system.

"""

from ._client import EventClient
from ._trigger import Trigger
from ..models import (AchievementAdded, BattleRankUp, Death, Event,
                      FacilityControl, GainExperience, ItemAdded,
                      MetagameEvent, PlayerFacilityCapture,
                      PlayerFacilityDefend, PlayerLogin, PlayerLogout,
                      SkillAdded, VehicleDestroy, ContinentLock,
                      ContinentUnlock)

__all__ = [
    'Event',
    'EventClient',
    'Trigger',

    # Event subclasses
    'AchievementAdded',
    'BattleRankUp',
    'ContinentLock',
    'ContinentUnlock',
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
