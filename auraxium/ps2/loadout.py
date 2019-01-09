from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import InterimDatatype, StaticDatatype
from .faction import Faction
from .profile import Profile


class Loadout(StaticDatatype):
    """A loadout in PlanetSide 2.

    A loadout is defined by the class and faction of a character. Examples
    are "TR Infiltrator", "VS Heavy Assault" or "NC MAX". I am uncertain
    whether these are worth giving access to.

    """

    _collection = 'loadout'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.faction = Faction(data['faction_id'])
        self.name = data['code_name']
        self.profile = Profile(data['profile_id'])
