from ..census import Query
from ..datatypes import StaticDatatype


class Faction(StaticDatatype):
    """Represents a faction in PlanetSide 2.

    Factions are static datatypes. Each one should only need to be
    initialized once.

    """

    _collection = 'faction'

    def __init__(self, id, data_override=None):
        self.id = id
        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.name = data.get('name')
        self.playable = True if data.get('user_selectable') == '1' else False

        # As of the writing of this module, Nanite Systems does not have a tag.
        # As this might change with the introduction of combat robots, I wrote
        # this section in a way that should be able to handle that gracefully.
        self.tag = 'NS' if data.get(
            'code_tag') == 'None' else data.get('code_tag')

        super()._add_to_cache(self)

    def __str__(self):
        return 'Faction (ID: {}, Name: "{}")'.format(
            self.id, self.name['en'])
