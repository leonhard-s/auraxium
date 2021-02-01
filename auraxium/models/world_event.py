from typing import Literal

from auraxium.models.eventmodel import Event


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
    # metagame_event_id: int    # TODO deal with this in subclasses
    metagame_event_state: int
