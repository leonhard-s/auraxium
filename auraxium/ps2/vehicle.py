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

        self.cost = data.get('cost')
        self.description = data.get('description')
        self.image = Image(data.get('image_set_id'))
        self.image_set = ImageSet(data.get('image_id'))
        self.name = data.get('name')
        self.resource = Currency(data.get('cost_resource_id'))
        self.type = data.get('type')
        self.type_name = data.get('type_name')

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

        self.description = data.get('description')
        self.faction = Faction(data.get('faction_id'))
        self.slot_id = data.get('slot_id')
        self.vehicle = Vehicle(data.get('vehicle_id'))
