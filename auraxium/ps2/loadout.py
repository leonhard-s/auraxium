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
    _join = ['faction', 'profile']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.faction = Faction(data.get('faction_id'),
                               data_override=data.get('faction'))
        self.name = data.get('code_name')
        self.profile = Profile(data.get('profile_id'),
                               data_override=data.get('profile'))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Loadout (ID: {}, Name: "{}")'.format(
            self.id, self.name)
