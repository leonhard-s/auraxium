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

    def __init__(self, id):
        self.id = id
        data = super(Profile, self).get_data(self, id_field_name='profile_id')
        self.description = data.get('description')

        @property
        def armor_info(self):
            pass

        @property
        def resist_info(self):
            pass

    def __str__(self):
        return 'Profile (ID: {}, Description: "{}")'.format(
            self.id, self.description)
