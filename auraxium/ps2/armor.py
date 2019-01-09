from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ArmorFacing(StaticDatatype):
    _collection = 'armor_facing'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.description = data['description']


class ArmorInfo(InterimDatatype):
    _collection = 'armor_info'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.armor_facing = ArmorFacing(data['armor_facing_id'])
        self.armor_percent = int(data['armor_percent'])

        # This field has been set to NULL for every single entry. I commented
        # it out for the time being.
        # self.armor_amount = int(data['armor_amount'])

        self.description = data['description']
