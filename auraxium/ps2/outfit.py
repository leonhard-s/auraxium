from datetime import datetime

from ..census import Query
from ..datatypes import InterimDatatype
from .character import Character


class Outfit(InterimDatatype):
    _cache_size = 10  # kept low as player stats might be added
    _collection = 'outfit'

    def __init__(self, id):
        self.id = id
        data = super(Outfit, self).get_data(self)

        self.alias = data.get('alias')
        self.leader = Character(data.get('leader_character_id'))
        self.member_count = data.get('member_count')
        self.name = data.get('name')
        self.time_created = datetime.utcfromtimestamp(int(
            data.get('time_created')))

        @property
        def members(self):
            pass

    def __str__(self):
        return 'Outfit (ID: {}, Tag: "{}", Name[en]: "{}")'.format(
            self.id, self.alias, self.name)


class OutfitMember(InterimDatatype):
    _cache_size = 500
    _collection = 'outfit_member'

    def __init__(self, id):
        self.id = id
        data = super(OutfitMember, self).get_data(self)

        self.character = Character(data.get('character_id'))
        self.member_since = datetime.utcfromtimestamp(int(
            data.get('member_since')))
        self.rank = data.get('rank')
        self.rank_ordinal = data.get('rank_ordinal')

    def __str__(self):
        return 'OutfitMember (ID: {}, Name: "{}")'.format(
            self.id, self.character.name)


class OutfitRank(InterimDatatype):
    _cache_size = 500
    _collection = 'outfit_rank'

    def __init__(self, id):
        self.id = id
        data = super(OutfitRank, self).get_data(self)

        self.description = data.get('description')
        self.name = data.get('name')
        self.ordinal = data.get('ordinal')
        self.outfit = Outfit(data.get('outfit_id'))

    def __str__(self):
        return 'OutfitRank (ID: {}, Name: "{}")'.format(
            self.id, self.name)
