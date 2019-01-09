from datetime.datetime import utcfromtimestamp

from ..census import Query
from ..datatypes import InterimDatatype
from .character import Character


class Outfit(InterimDatatype):
    _cache_size = 10  # kept low as player stats might be added
    _collection = 'outfit'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.alias = data['alias']
        self.leader = Character(data['leader_character_id'])
        self.member_count = int(data['member_count'])
        self.name = data['name']
        self.time_created = utcfromtimestamp(int(data['time_created']))

        @property
        def members(self):
            pass


class OutfitMember(InterimDatatype):
    _cache_size = 500
    _collection = 'outfit_member'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.character = Character(data['character_id'])
        self.member_since = utcfromtimestamp(int(data['member_since']))
        self.rank = data['rank']
        self.rank_ordinal = data['rank_ordinal']


class OutfitRank(InterimDatatype):
    _cache_size = 500
    _collection = 'outfit_rank'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description']
        self.name = data['name']
        self.ordinal = int(data['ordinal'])
        self.outfit = Outfit(data['outfit_id'])
