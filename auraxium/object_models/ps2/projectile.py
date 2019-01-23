from ..datatypes import CachableDataType, EnumeratedDataType


class Projectile(CachableDataType):
    """A projectile.

    Anything that moves predictably, such as bullets or grenades.

    """

    _collection = 'projectile'

    def __init__(self, id):
        self.id = id

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
        return ProjectileFlightType.get(id=self._projectile_flight_type_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._projectile_flight_type_id = d['projectile_flight_type_id']
        self.speed = d.get('speed')
        self.speed_max = d.get('speed_max')
        self.acceleration = d.get('acceleration')
        self.turn_rate = d.get('turn_rate')
        self.lifespan = d.get('lifespan')
        self.turn_rate = d.get('turn_rate')
        self.drag = d.get('drag')
        self.gravity = d.get('gravity')
        self.lockon_acceleration = d.get('lockon_acceleration')
        self.lockon_lifespan = d.get('lockon_lifespan')
        self.arm_distance = d.get('arm_distance')
        self.tether_distance = d.get('tether_distance')
        self.detonate_distance = d.get('detonate_distance')
        self.is_sticky = d.get('sticky')
        self.sticks_to_players = d.get('sticks_to_players')
        self.lockon_lose_angle = d.get('lockon_lose_angle')
        self.lockon_seek_in_flight = d.get('lockon_seek_in_flight')


class ProjectileFlightType(EnumeratedDataType):
    """A flight type for a projectile.

    Lists the flight types available for projectiles, such as "hurled across
    the room", "hitscan" or "pseudo-ballistic".

    """

    _collection = 'projectile_flight_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
