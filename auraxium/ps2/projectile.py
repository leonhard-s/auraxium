"""Projectile and flight type class definitions."""

import dataclasses
import enum
from typing import Optional

from ..base import Cached, Ps2Data
from ..types import CensusData
from ..utils import optional


class ProjectileFlightType(enum.IntEnum):
    """A projectile flight type."""

    BALLISTIC = 1
    TRUE_BALLISTIC = 3
    DYNAMIC = 9
    PROXIMITY_DETONATE = 10


@dataclasses.dataclass(frozen=True)
class ProjectileData(Ps2Data):
    """Data class for :class:`auraxium.ps2.projectile.Projectile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
            int(data['projectile_id']),
            int(data['projectile_flight_type_id']),
            int(data['speed']),
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


class Projectile(Cached, cache_size=100, cache_ttu=60.0):
    """A projectile fired by a fire mode."""

    collection = 'projectile'
    data: ProjectileData
    id_field = 'projectile_id'

    @property
    def flight_type(self) -> ProjectileFlightType:
        """Return the flight type of the projectile."""
        return ProjectileFlightType(self.data.projectile_flight_type_id)

    @staticmethod
    def _build_dataclass(data: CensusData) -> ProjectileData:
        return ProjectileData.from_census(data)
