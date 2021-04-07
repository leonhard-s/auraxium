"""Data classes for :mod:`auraxium.ps2.states`."""

from typing import Optional

from .base import RESTPayload

__all__ = [
    'PlayerStateGroup'
]

# pylint: disable=too-few-public-methods


class PlayerStateGroup(RESTPayload):
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
    cof_grow_rate: Optional[float] = None
    cof_max: float
    cof_min: float
    cof_recovery_delay_ms: Optional[int] = None
    cof_recovery_rate: float
    cof_shots_before_penalty: Optional[int] = None
    cof_recovery_delay_threshold: Optional[int] = None
    cof_turn_penalty: Optional[int] = None
