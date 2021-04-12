"""Data classes for :mod:`auraxium.ps2._states`."""

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

    .. attribute:: player_state_group_id
       :type: int

       The ID of the player state group.

    .. attribute:: player_state_id
       :type: int

       The :class:`~auraxium.ps2.PlayerState` enum value of this entry.

    .. attribute:: can_iron_sight
       :type: bool

       Whether ADS is allowed in this state.

    .. attribute:: cof_grow_rate
       :type: float | None

       Cone of fire growth per shot.

    .. attribute:: cof_max
       :type: float

       The maximum cone-of-fire for this state.

    .. attribute:: cof_min
       :type: float

       The minimum cone-of-fire for this state.

    .. attribute:: cof_recovery_delay_ms
       :type: int | None

       The time before the cone-of-fire will start to reset after the
       user stopped firing.

    .. attribute:: cof_recovery_rate
       :type: int | None

       The speed at which the cone-of-fire will return to its starting
       value after the user stopped firing.

    .. attribute:: cof_shots_before_penalty
       :type: int | None

       The number of "free shots" before cone-of-fire penalties are
       applied.

    .. attribute:: cof_recovery_delay_threshold
       :type: int | None

       (Not yet documented)

    .. attribute:: cof_turn_penalty
       :type: int | None

       (Not yet documented)
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
