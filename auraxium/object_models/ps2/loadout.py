from ..datatypes import EnumeratedDataType
from .faction import Faction
from .profile import Profile


class Loadout(EnumeratedDataType):
    """A loadout in PlanetSide 2.

    A loadout is defined by the class and faction of a character. Examples
    are "TR Infiltrator", "VS Heavy Assault" or "NC MAX".

    """

    _collection = 'loadout'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._faction_id = None
        self.name = None
        self._profile_id = None

    # Define properties
    @property
    def faction(self):
        return Faction.get(id=self._faction_id)

    @property
    def profile(self):
        return Profile.get(id=self._profile_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._faction_id = d['faction_id']
        self.name = d['code_name']
        self._profile_id = d['profile_id']
