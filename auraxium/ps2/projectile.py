"""Projectile and flight type class definitions."""

import enum
from typing import Optional

from ..base import Cached
from ..models import ProjectileData


class ProjectileFlightType(enum.IntEnum):
    """A projectile flight type."""

    BALLISTIC = 1
    TRUE_BALLISTIC = 3
    DYNAMIC = 9
    PROXIMITY_DETONATE = 10


class Projectile(Cached, cache_size=100, cache_ttu=60.0):
    """A projectile fired by a fire mode.

    Attributes:
        projectile_id: The unique ID of this projectile.
        projectile_flight_type_id: The ID of the associated
            :class:`ProjectileFlightType`.
        speed: The projectile speed in meters per second.
        speed_max: The maximum speed of the projectile; used with
            :attr:`acceleration`.
        acceleration: The acceleration of the projectile in meters
            per second per second.
        turn_rate: The turn rate of the projectile in degrees per
            second.
        lifespan: The time after which the projectile will be
            destroyed if it has not hit a target. Effectively limits
            the maximum distance travelled.
        drag: The drag applied to the projectile.
        gravity: The affect on gravity on the projectile.
        lockon_acceleration: (Not yet documented)
        lockon_lifespan: The life span of the projectile after it has
            locked onto a target.
        arm_distance: The minimum distance travelled for the projectile
            to be armed. Used to increase the Archer's damage on range.
        tether_distance: (Not yet documented)
        detonate_distance: The travelled distance after which the
            projectile will detonate.
        detonate_on_contact: Whether the projectile will explode when
            hitting a target. False for grenades and other bouncing
            projectiles.
        sticky: Whether the projectile will stick to objects.
        sticks_to_players: Whether the projectile will stick to
            players.
        lockon_lose_angle: The angle at which the projectile will lose
            its lock if the target's turn speed exceeds its own.
        lockon_seek_in_flight: Whether the projectile will continue to
            follow its target after launch.

    """

    collection = 'projectile'
    data: ProjectileData
    dataclass = ProjectileData
    id_field = 'projectile_id'

    # Type hints for data class fallback attributes
    projectile_id: int
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
