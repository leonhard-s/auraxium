from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Projectile(InterimDatatype):
    _cache_size = 100
    _collection = 'projectile'

    def __init__(self, id):
        self.id = id
        data = super(Projectile, self).get_data(self)

        self.flight_type = ProjectileFlightType(
            data.get('projectile_flight_type_id'))
        self.speed = data.get('speed')
        self.speed_max = data.get('speed_max')
        self.acceleration = data.get('acceleration')
        self.turn_rate = data.get('turn_rate')
        self.lifespan = data.get('lifespan')
        self.turn_rate = data.get('turn_rate')
        self.drag = data.get('drag')
        self.gravity = data.get('gravity')
        self.lockon_acceleration = data.get('lockon_acceleration')
        self.lockon_lifespan = data.get('lockon_lifespan')
        self.arm_distance = data.get('arm_distance')
        self.tether_distance = data.get('tether_distance')
        self.detonate_distance = data.get('detonate_distance')
        self.sticky = data.get('sticky')
        self.sticks_to_players = data.get('sticks_to_players')
        self.lockon_lose_angle = data.get('lockon_lose_angle')
        self.lockon_seek_in_flight = data.get('lockon_seek_in_flight')

    def __str__(self):
        return 'Projectile (ID: {})'.format(self.id)


class ProjectileFlightType(StaticDatatype):
    _collection = 'projectile_flight_type'

    def __init__(self, id):
        self.id = id
        data = super(ProjectileFlightType, self).get_data(self)
        self.description = data.get('description')

    def __str__(self):
        return 'ProjectileFlightType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
