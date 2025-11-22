"""Data classes for :mod:`auraxium.ps2._projectile`."""

from .base import RESTPayload

__all__ = [
    'ProjectileData'
]


class ProjectileData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Projectile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    projectile_id: int
    projectile_flight_type_id: int
    speed: int
    speed_max: int | None = None
    acceleration: int | None = None
    turn_rate: int | None = None
    lifespan: float | None = None
    drag: float | None = None
    gravity: float | None = None
    lockon_acceleration: float | None = None
    lockon_lifespan: float | None = None
    arm_distance: float | None = None
    tether_distance: float | None = None
    detonate_distance: float | None = None
    detonate_on_contact: bool | None = None
    sticky: bool | None = None
    sticks_to_players: bool | None = None
    lockon_lose_angle: int | None = None
    lockon_seek_in_flight: bool | None = None
