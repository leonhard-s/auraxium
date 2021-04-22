"""Player state group class definitions."""

import enum
from ..models import PlayerStateGroup

__all__ = [
    'PlayerState',
    'PlayerStateGroup'
]


class PlayerState(enum.IntEnum):
    """A player state.

    These are used to apply the situational weapon stats depending on
    the player state, e.g. running, springing, crouching, etc.

    Values:::

       STANDING         = 0
       CROUCHING        = 1
       STANDING_MOVING  = 2
       SPRINTING        = 3
       FALLING_LONG     = 4
       CROUCHING_MOVING = 5
    """

    STANDING = 0
    CROUCHING = 1
    STANDING_MOVING = 2
    SPRINTING = 3
    FALLING_LONG = 4
    CROUCHING_MOVING = 5
