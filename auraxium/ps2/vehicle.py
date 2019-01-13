from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .currency import Currency
from .faction import Faction
from .image import Image, ImageSet


class Vehicle(StaticDatatype):
    _collection = 'vehicle'
    _join = 'image_set'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.cost = data.get('cost')
        self.description = data.get('description')
        self.image = Image(data.get('image_id'))
        self.image_set = ImageSet(
            data.get('image_set_id'), data_override=data.get('image_set'))
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

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Vehicle (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])


class VehicleAttachment(InterimDatatype):
    _cache_size = 100
    _collection = 'vehicle_attachment'
    _join = ['faction', 'vehicle']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.faction = Faction(data.get('faction_id'),
                               data_override=data.get('faction'))
        self.slot_id = data.get('slot_id')
        self.vehicle = Vehicle(data.get('vehicle_id'),
                               data_override=data.get('vehicle'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'VehicleAttachment (ID: {}, Description: "{}")'.format(
            self.id, self.description)
