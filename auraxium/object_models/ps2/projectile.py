"""Defines projectile-related data types for PlanetSide 2."""

from ..datatypes import DataType


class Projectile(DataType):  # pylint: disable=too-many-instance-attributes
    """A projectile.

    Anything that moves predictably, such as bullets or grenades.

    """

    _collection = 'projectile'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.acceleration = None
        self.arm_distance = None
        self.detonate_distance = None
        self.drag = None
        self.gravity = None
        self.is_sticky = None
        self.lifespan = None
        self.lockon_acceleration = None
        self.lockon_lifespan = None
        self.lockon_lose_angle = None
        self.lockon_seek_in_flight = None
        self._projectile_flight_type_id = None
        self.sticks_to_players = None
        self.speed = None
        self.speed_max = None
        self.tether_distance = None
        self.turn_rate = None

    # Define properties
    @property
    def projectile_flight_type(self):
        """The flight type of the projectile."""
        return ProjectileFlightType.get(id_=self._projectile_flight_type_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._projectile_flight_type_id = data_dict['projectile_flight_type_id']
        self.speed = data_dict.get('speed')
        self.speed_max = data_dict.get('speed_max')
        self.acceleration = data_dict.get('acceleration')
        self.turn_rate = data_dict.get('turn_rate')
        self.lifespan = data_dict.get('lifespan')
        self.turn_rate = data_dict.get('turn_rate')
        self.drag = data_dict.get('drag')
        self.gravity = data_dict.get('gravity')
        self.lockon_acceleration = data_dict.get('lockon_acceleration')
        self.lockon_lifespan = data_dict.get('lockon_lifespan')
        self.arm_distance = data_dict.get('arm_distance')
        self.tether_distance = data_dict.get('tether_distance')
        self.detonate_distance = data_dict.get('detonate_distance')
        self.is_sticky = data_dict.get('sticky')
        self.sticks_to_players = data_dict.get('sticks_to_players')
        self.lockon_lose_angle = data_dict.get('lockon_lose_angle')
        self.lockon_seek_in_flight = data_dict.get('lockon_seek_in_flight')


class ProjectileFlightType(DataType):
    """A flight type for a projectile.

    Lists the flight types available for projectiles, such as "hurled across
    the room", "hitscan" or "pseudo-ballistic".

    """

    _collection = 'projectile_flight_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')
