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

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']

        @property
        def armor_info(self):
            pass

        @property
        def resist_info(self):
            pass
