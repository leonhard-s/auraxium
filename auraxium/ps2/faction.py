from ..census import Query
from ..datatypes import StaticDatatype


class Faction(StaticDatatype):
    """Represents a faction in PlanetSide 2.

    Factions are static datatypes. Each one should only need to be
    initialized once.

    """

    _collection = 'faction'

    def __init__(self, id):
        self.id = id  # faction_id
        data = super(Faction, self).get_data(self)

        self.name = data['name']
        self.playable = True if data['user_selectable'] == '1' else False

        # As of the writing of this module, Nanite Systems does not have a tag.
        # As this might change with the introduction of combat robots, I wrote
        # this section in a way that should be able to handle that gracefully.
        self.tag = 'NS' if data['code_tag'] == 'None' else data['code_tag']
