from ..census import _CENSUS_BASE_URL, Query
from ..datatypes import EnumeratedDataType
from .faction import Faction
from .profile import Profile


class Loadout(EnumeratedDataType):
    """A loadout in PlanetSide 2.

    A loadout is defined by the class and faction of a character. Examples
    are "TR Infiltrator", "VS Heavy Assault" or "NC MAX".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self._faction_id = None
        self.name = None
        self._profile_id = None

        # Define properties
        @property
        def faction(self):
            try:
                return self._faction
            except AttributeError:
                self._faction = Faction.get(id=self._faction_id)
                return self._faction

        @property
        def profile(self):
            try:
                return self._profile
            except AttributeError:
                self._profile = Profile.get(id=self._profile_id)
                return self._profile

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self._faction_id = data['faction_id']
        self.name = data['code_name']
        self._profile_id = data['profile_id']
