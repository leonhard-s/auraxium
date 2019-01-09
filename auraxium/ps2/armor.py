from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ArmorFacing(StaticDatatype):
    _collection = 'armor_facing'

    def __init__(self, id):
        self.id = id
        data = super(ArmorFacing, self).get_data(self)

        self.description = data['description']


class ArmorInfo(InterimDatatype):
    _collection = 'armor_info'

    def __init__(self, id):
        self.id = id
        data = super(ArmorInfo, self).get_data(self)

        self.armor_facing = ArmorFacing(data['armor_facing_id'])
        self.armor_percent = int(data['armor_percent'])
        self.description = data['description']

        # This field has been set to NULL for every single entry. I commented
        # it out for the time being.
        # self.armor_amount = int(data['armor_amount'])
        pass
