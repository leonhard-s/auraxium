from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype


class ArmorFacing(StaticDatatype):
    _collection = 'armor_facing'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ArmorFacing (ID: {}, Description: "{}")'.format(
            self.name, self.description)


class ArmorInfo(InterimDatatype):
    _collection = 'armor_info'
    _join = 'armor_facing'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.armor_facing = ArmorFacing(
            data.get('armor_facing_id'), data_override=data.get('armor_facing'))
        self.armor_percent = data.get('armor_percent')
        self.description = data.get('description')

        # This field has been set to NULL for every single entry. I commented
        # it out for the time being.
        # self.armor_amount = data.get('armor_amount'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'ArmorInfo (ID: {}, Description: "{}")'.format(
            self.id, self.description)
