"""Projectile and flight type class definitions."""

import enum
from typing import Optional

from ..base import Cached
from ..models import ProjectileData

__all__ = [
    'Projectile',
    'ProjectileFlightType'
]


class ProjectileFlightType(enum.IntEnum):
    """A projectile flight type."""

    BALLISTIC = 1
    TRUE_BALLISTIC = 3
    DYNAMIC = 9
    PROXIMITY_DETONATE = 10


class Projectile(Cached, cache_size=100, cache_ttu=60.0):
    """A projectile fired by a fire mode.

    .. attribute:: id
       :type: int

       The unique ID of this projectile.

    .. attribute:: projectile_flight_type_id
       :type: int

       The ID of the associated
       :class:`auraxium.ps2.ProjectileFlightType`.

    .. attribute:: speed
       :type: int

       The projectile speed in meters per second.

    .. attribute:: speed_max
       :type: int | None

       The maximum speed of the projectile; used with
       :attr:`acceleration`.

    .. attribute:: acceleration
       :type: int | None

       The acceleration of the projectile in meters per second per
       second.

    .. attribute:: turn_rate
       :type: int | None

       The turn rate of the projectile in degrees per second.

    .. attribute:: lifespan
       :type: int | float

       The time after which the projectile will be destroyed if it ha
        not hit a target. Effectively limits  the maximum distance
        travelled.

    .. attribute:: drag
       :type: float | None

       The drag applied to the projectile.

    .. attribute:: gravity
       :type: float | None

       The affect on gravity on the projectile.

    .. attribute:: lockon_acceleration
       :type: float | None

       (Not yet documented)

    .. attribute:: lockon_lifespan
       :type: float | None

       The life span of the projectile after it has locked onto a
       target.

    .. attribute:: arm_distance
       :type: float | None

       The minimum distance travelled for the projectile to be armed.
       Used to increase the Archer's damage on range.

    .. attribute:: tether_distance
       :type: float | None

       (Not yet documented)

    .. attribute:: detonate_distance
       :type: float | None

       The travelled distance after which the projectile will detonate.

    .. attribute:: detonate_on_contact
       :type: bool | None

       Whether the projectile will explode when hitting a target. False
       for grenades and other bouncing projectiles.

    .. attribute:: sticky
       :type: bool | None

       Whether the projectile will stick to objects.

    .. attribute:: sticks_to_players
       :type: bool | None

       Whether the projectile will stick to players.

    .. attribute:: lockon_lose_angle
       :type: int | None

       The angle at which the projectile will lose its lock if the
       target's turn speed exceeds its own.

    .. attribute:: lockon_seek_in_flight
       :type: bool | None

       Whether the projectile will continue to follow its target after
       launch.
    """

    collection = 'projectile'
    data: ProjectileData
    id_field = 'projectile_id'
    _model = ProjectileData

    # Type hints for data class fallback attributes
    id: int
    projectile_flight_type_id: int
    speed: int
    speed_max: Optional[int]
    acceleration: Optional[int]
    turn_rate: Optional[int]
    lifespan: Optional[float]
    drag: Optional[float]
    gravity: Optional[float]
    lockon_acceleration: Optional[float]
    lockon_lifespan: Optional[float]
    arm_distance: Optional[float]
    tether_distance: Optional[float]
    detonate_distance: Optional[float]
    detonate_on_contact: Optional[bool]
    sticky: Optional[bool]
    sticks_to_players: Optional[bool]
    lockon_lose_angle: Optional[int]
    lockon_seek_in_flight: Optional[bool]

    @property
    def flight_type(self) -> ProjectileFlightType:
        """Return the flight type of the projectile."""
        return ProjectileFlightType(self.data.projectile_flight_type_id)
