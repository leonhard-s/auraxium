"""Data classes for :mod:`auraxium.ps2.projectile`."""

from typing import Optional

from ._base import RESTPayload

__all__ = [
    'ProjectileData'
]

# pylint: disable=too-few-public-methods


class ProjectileData(RESTPayload):
    """Data class for :class:`auraxium.ps2.projectile.Projectile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
