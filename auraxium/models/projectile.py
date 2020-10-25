"""Data classes for :mod:`auraxium.ps2.projectile`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'ProjectileData'
]


class ProjectileData(Ps2Data):
    """Data class for :class:`auraxium.ps2.projectile.Projectile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

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

    projectile_id: int
    projectile_flight_type_id: int
    speed: int
    speed_max: Optional[int] = None
    acceleration: Optional[int] = None
    turn_rate: Optional[int] = None
    lifespan: Optional[float] = None
    drag: Optional[float] = None
    gravity: Optional[float] = None
    lockon_acceleration: Optional[float] = None
    lockon_lifespan: Optional[float] = None
    arm_distance: Optional[float] = None
    tether_distance: Optional[float] = None
    detonate_distance: Optional[float] = None
    detonate_on_contact: Optional[bool] = None
    sticky: Optional[bool] = None
    sticks_to_players: Optional[bool] = None
    lockon_lose_angle: Optional[int] = None
    lockon_seek_in_flight: Optional[bool] = None
