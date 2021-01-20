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
    """A projectile fired by a fire mode."""

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
