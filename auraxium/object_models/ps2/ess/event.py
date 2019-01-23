from .ps2 import (AchievementEarned, BattleRankUp, ContinentLock,
                  ContinentUnlock, Death, FacilityControl, GainExperience,
                  ItemAdded, MetagameEvent, PlayerFacilityCapture,
                  PlayerFacilityDefend, PlayerLogin, PlayerLogout, SkillAdded,
                  VehicleDestroy)
from ...exceptions import UnknownEventTypeError


class EventListener():
    """An event listener.

    Links one or more events to an event message. This object can be
    modified at any point to adjust its triggering behaviour.

    """

    def __init__(self, events, characters=None, worlds=None):
        self.characters = characters
        self.events = events
        self.message = None
        self.worlds = worlds

    def evaluate(self, event):
        """Returns True if the event passed fulfills the critera."""
        if event.name not in self.events:
            return False
        try:
            if self.worlds is not None and event.world_id not in self.worlds:
                return False
        except AttributeError:
            pass
        try:
            if event.character.id not in self.characters:
                return False
        except AttributeError:
            pass
        try:
            if (event.attacker_character.id not in self.characters
                    and event.victim_character.id not in self.characters):
                return False
        except AttributeError:
            pass
        return True

    def subscribe(self):
        data = {'action': 'subscribe',
                'characters': self.characters if self.characters is not None else ['all'],
                'eventNames': self.events if self.events is not None else ['all'],
                "worlds": self.worlds if self.worlds is not None else ['all'],
                'service': 'event'}
        return data


def get_event(payload):
    """Retrieves the object representation of the event payload passed.

    Searches for an event matching the name defined in the payload dictionary
    and returns a populated instance.

    Raises an "UnknownEventTypeError" if no suitable event object can be found.

    """

    # Links the event names with their corresponding object types
    EVENTS = {'AchievementEarned': AchievementEarned,
              'BattleRankUp': BattleRankUp,
              'ContinentLock': ContinentLock,
              'ContinentUnlock': ContinentUnlock,
              'Death': Death,
              'FacilityControl': FacilityControl,
              'GainExperience': GainExperience,
              'ItemAdded': ItemAdded,
              'MetagameEvent': MetagameEvent,
              'PlayerFacilityCapture': PlayerFacilityCapture,
              'PlayerFacilityDefend': PlayerFacilityDefend,
              'PlayerLogin': PlayerLogin,
              'PlayerLogout': PlayerLogout,
              'SkillAdded': SkillAdded,
              'VehicleDestroy': VehicleDestroy}

    try:
        return EVENTS[payload['event_name']](payload)
    except KeyError:
        raise UnknownEventTypeError
