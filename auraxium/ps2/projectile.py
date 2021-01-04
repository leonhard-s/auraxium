"""Projectile and flight type class definitions."""

import enum

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

    @property
    def flight_type(self) -> ProjectileFlightType:
        """Return the flight type of the projectile."""
        return ProjectileFlightType(self.data.projectile_flight_type_id)
