from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class Projectile(InterimDatatype):
    _cache_size = 100
    _collection = 'projectile'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.flight_type = ProjectileFlightType(
            data['projectile_flight_type_id'])
        self.speed = float(data['speed']) if data['speed'] != 'NULL' else None
        self.speed_max = float(
            data['speed_max']) if data['speed_max'] != 'NULL' else None
        self.acceleration = float(
            data['acceleration']) if data['acceleration'] != 'NULL' else None
        self.turn_rate = float(
            data['turn_rate']) if data['turn_rate'] != 'NULL' else None
        self.lifespan = float(
            data['lifespan']) if data['lifespan'] != 'NULL' else None
        self.turn_rate = float(
            data['turn_rate']) if data['turn_rate'] != 'NULL' else None
        self.drag = float(data['drag']) if data['drag'] != 'NULL' else None
        self.gravity = float(
            data['gravity']) if data['gravity'] != 'NULL' else None
        self.lockon_acceleration = float(
            data['lockon_acceleration']) if data['lockon_acceleration'] != 'NULL' else None
        self.lockon_lifespan = float(
            data['lockon_lifespan']) if data['lockon_lifespan'] != 'NULL' else None
        self.arm_distance = float(
            data['arm_distance']) if data['arm_distance'] != 'NULL' else None
        self.tether_distance = float(
            data['tether_distance']) if data['tether_distance'] != 'NULL' else None
        self.detonate_distance = float(
            data['detonate_distance']) if data['detonate_distance'] != 'NULL' else None
        self.sticky = float(
            data['sticky']) if data['sticky'] != 'NULL' else None
        self.sticks_to_players = float(
            data['sticks_to_players']) if data['sticks_to_players'] != 'NULL' else None
        self.lockon_lose_angle = float(
            data['lockon_lose_angle']) if data['lockon_lose_angle'] != 'NULL' else None
        self.lockon_seek_in_flight = float(
            data['lockon_seek_in_flight']) if data['lockon_seek_in_flight'] != 'NULL' else None


class ProjectileFlightType(StaticDatatype):
    _collection = 'projectile_flight_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
