from typing import Literal

from pydantic import Field, validator

from ..event import Event

__all__ = [
    "ContinentLock",
    "ContinentUnlock",
    "FacilityControl",
    "MetagameEvent"
]


class ContinentLock(Event):
    event_name: Literal['ContinentLock']
    triggering_faction: int
    previous_faction: int
    vs_population: int
    nc_population: int
    tr_population: int
    metagame_event_id: int
    event_type: int


class ContinentUnlock(Event):
    event_name: Literal['ContinentUnlock']
    triggering_faction: int
    previous_faction: int
    vs_population: int
    nc_population: int
    tr_population: int
    metagame_event_id: int
    event_type: int


class FacilityControl(Event):
    event_name: Literal['FacilityControl']
    duration_held: int
    facility_id: int
    new_faction_id: int
    old_faction_id: int
    outfit_id: int


class MetagameEvent(Event):
    event_name: Literal['MetagameEvent']
    experience_bonus: int
    faction_nc: float  # Percentage of territory captured, as far as I can tell
    faction_tr: float
    faction_vs: float
    metagame_event_id: int
    metagame_event_state: int
    zone_id = Field(default=-1)

    @validator('zone_id')
    def generate_zone_id(cls, zone_id):
        if zone_id == -1:
            return zone_id_from_event_id(0) # TODO this doesn't work because we don't have access to metagame event id


def zone_id_from_event_id(metagame_event_id: int):
    pass


