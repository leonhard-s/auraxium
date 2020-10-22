"""Data classes for :mod:`auraxium.ps2.projectile`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData, optional

__all__ = [
    'ProjectileData'
]


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'ProjectileData':
        return cls(
            int(data.pop('projectile_id')),
            int(data.pop('projectile_flight_type_id')),
            int(data.pop('speed')),
            optional(data, 'speed_max', int),
            optional(data, 'acceleration', int),
            optional(data, 'turn_rate', int),
            optional(data, 'lifespan', float),
            optional(data, 'drag', float),
            optional(data, 'gravity', float),
            optional(data, 'lockon_acceleration', float),
            optional(data, 'lockon_lifespan', float),
            optional(data, 'arm_distance', float),
            optional(data, 'tether_distance', float),
            optional(data, 'detonate_distance', float),
            optional(data, 'detonate_on_contact', bool),
            optional(data, 'sticky', bool),
            optional(data, 'sticks_to_players', bool),
            optional(data, 'lockon_lose_angle', int),
            optional(data, 'lockon_seek_in_flight', bool))
