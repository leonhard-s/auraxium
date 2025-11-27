"""Projectile and flight type class definitions."""

import enum
from ..base import Cached
from ..collections import ProjectileData

__all__ = [
    'Projectile',
    'ProjectileFlightType'
]


class ProjectileFlightType(enum.IntEnum):
    """A projectile flight type.
    structable items.

    Values:::

       BALLISTIC = 1
       TRUE_BALLISTIC = 3
       DYNAMIC = 9
       PROXIMITY_DETONATE = 10
    """

    BALLISTIC = 1
    TRUE_BALLISTIC = 3
    DYNAMIC = 9
    PROXIMITY_DETONATE = 10


class Projectile(Cached, cache_size=100, cache_ttu=60.0):
    """A projectile fired by a fire mode.

    .. attribute:: id
       :type: int

       The unique ID of this projectile. In the API payload, this
       field is called ``projectile_id``.

    .. attribute:: projectile_flight_type_id
       :type: int

       The ID of the projectile's
       :class:`~auraxium.ps2.ProjectileFlightType`.

       .. seealso::

          :meth:`flight_type` -- The enum value of the projectile's
          flight type.

    .. attribute:: speed
       :type: int

       The projectile speed in meters per second.

       .. note::

          A :class:`~auraxium.ps2.FireMode` can override this value via
          its :attr:`~auraxium.ps2.FireMode.projectile_speed_override`
          field.

          It is therefore recommended to use that field instead, if
          available.

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

       The atmospheric drag applied to the projectile.

    .. attribute:: gravity
       :type: float | None

       The affect on gravity on the projectile.

    .. attribute:: lockon_acceleration
       :type: float | None

       Not yet documented.

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

       Not yet documented.

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
    speed_max: int | None
    acceleration: int | None
    turn_rate: int | None
    lifespan: float | None
    drag: float | None
    gravity: float | None
    lockon_acceleration: float | None
    lockon_lifespan: float | None
    arm_distance: float | None
    tether_distance: float | None
    detonate_distance: float | None
    detonate_on_contact: bool | None
    sticky: bool | None
    sticks_to_players: bool | None
    lockon_lose_angle: int | None
    lockon_seek_in_flight: bool | None

    @property
    def flight_type(self) -> ProjectileFlightType:
        """Return the flight type of the projectile."""
        return ProjectileFlightType(self.data.projectile_flight_type_id)
