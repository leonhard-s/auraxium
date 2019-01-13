from ..census import Query
from ..datatypes import StaticDatatype
from .armor import ArmorInfo


class Profile(StaticDatatype):
    """An entity in PlanetSide 2.

    If you can shoot it, it's one of these.
    I once again assumed that profile_2 is a straight upgrade over profile.
    I am probably wrong.

    """

    _collection = 'profile_2'
    _id_field = 'profile_id'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')

        @property
        def armor_info(self):
            pass

        @property
        def resist_info(self):
            pass

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Profile (ID: {}, Description: "{}")'.format(
            self.id, self.description)
