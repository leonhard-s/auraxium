"""Player state group class definitions."""

import dataclasses
import enum
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional


class PlayerState(enum.IntEnum):
    """A player state.

    These are used to apply the situational weapon stats depending on
    the player state, e.g. running, springing, crouching, etc.
    """

    STANDING = 0
    CROUCHING = 1
    STANDING_MOVING = 2
    SPRINTING = 3
    FALLING_LONG = 4
    CROUCHING_MOVING = 5


@dataclasses.dataclass(frozen=True)
class PlayerStateGroup(Ps2Data):
    """A fire-mode-specific state group.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
            int(data['player_state_group_id']),
            int(data['player_state_id']),
            bool(int(data['can_iron_sight'])),
            optional(data, 'cof_grow_rate', float),
            float(data['cof_max']),
            float(data['cof_min']),
            optional(data, 'cof_recovery_delay_ms', int),
            float(data['cof_recovery_rate']),
            optional(data, 'cof_shots_before_penalty', int),
            optional(data, 'cof_recovery_delay_threshold', int),
            optional(data, 'cof_turn_penalty', int))
