"""Data classes for :mod:`auraxium.ps2.states`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional

__all__ = [
    'PlayerStateGroup'
]


@dataclasses.dataclass(frozen=True)
class PlayerStateGroup(Ps2Data):
    """A fire-mode-specific state group.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        player_state_group_id: The ID of the player state group.
        player_state_id: The ID of the player state for this entry.
        can_iron_sight: Whether ADS is allowed in this state.
        cof_grow_rate: Cone of fire growth per shot.
        cof_max: The maximum cone-of-fire for this state.
        cof_min: The minimum cone-of-fire for this state.
        cof_recovery_delay_ms: The time before the cone-of-fire will
            start to reset after the user stopped firing.
        cof_recovery_rate: The speed at which the cone-of-fire will
            return to its starting value after the user stopped firing.
        cof_shots_before_penalty: (Not yet documented)
        cof_recovery_delay_threshold: (Not yet documented)
        cof_turn_penalty: (Not yet documented)

    """

    player_state_group_id: int
    player_state_id: int
    can_iron_sight: bool
    cof_grow_rate: Optional[float]
    cof_max: float
    cof_min: float
    cof_recovery_delay_ms: Optional[int]
    cof_recovery_rate: float
    cof_shots_before_penalty: Optional[int]
    cof_recovery_delay_threshold: Optional[int]
    cof_turn_penalty: Optional[int]

    @classmethod
    def from_census(cls, data: CensusData) -> 'PlayerStateGroup':
        return cls(
            int(data.pop('player_state_group_id')),
            int(data.pop('player_state_id')),
            bool(int(data.pop('can_iron_sight'))),
            optional(data, 'cof_grow_rate', float),
            float(data.pop('cof_max')),
            float(data.pop('cof_min')),
            optional(data, 'cof_recovery_delay_ms', int),
            float(data.pop('cof_recovery_rate')),
            optional(data, 'cof_shots_before_penalty', int),
            optional(data, 'cof_recovery_delay_threshold', int),
            optional(data, 'cof_turn_penalty', int))
