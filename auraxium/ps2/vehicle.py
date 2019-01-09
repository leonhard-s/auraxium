from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .currency import Currency
from .faction import Faction
from .image import Image, ImageSet


class Vehicle(StaticDatatype):
    _collection = 'vehicle'

    def __init__(self, id):
        self.id = id
        data = super(Vehicle, self).get_data(self)

        self.cost = int(data['cost'])
        self.description = data['description'][next(iter(data['description']))]
        self.image = Image(data['image_set_id'])
        self.image_set = ImageSet(data['image_id'])
        self.name = data['name'][next(iter(data['name']))]
        self.resource = Currency(data['cost_resource_id'])
        self.type = int(data['type'])
        self.type_name = data['type_name']

        @property
        def faction(self):
            pass

        @property
        def skill_set(self):
            pass


class VehicleAttachment(InterimDatatype):
    _cache_size = 100
    _collection = 'vehicle_attachment'

    def __init__(self, id):
        self.id = id
        data = super(VehicleAttachment, self).get_data(self)

        self.description = data['description']
        self.faction = Faction(data['faction_id'])
        self.slot_id = int(data['slot_id'])
        self.vehicle = Vehicle(data['vehicle_id'])
