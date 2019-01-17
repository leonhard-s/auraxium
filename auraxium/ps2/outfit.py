from datetime import datetime

from ..census import Query
from ..datatypes import CachableDataType
from .character import Character


class Outfit(CachableDataType):
    """Represents a PS2 outfit.

    An outfit is a group of players. The individual player information needs to be resolved further.

    """

    _collection = 'outfit'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.alias = None
        self._leader_id = None
        self.member_count = None
        self.name = None
        self.date_created = None

    # Define properties
    @property
    def leader(self):
        try:
            return self._leader
        except AttributeError:
            self._leader = Character.get(id=self._leader_id)
            return self._leader

    @property
    def members(self):
        try:
            return self._members
        except AttributeError:
            q = Query(type='outfit_member')
            d = q.add_filter(field='outfit_id', value=self.id).get()
            self._members = OutfitMember.list(ids=[i['profile_id'] for i in d])
            return self._members

    @staticmethod
    def get_by_name(name, ignore_case=True):
        # Generate request
        q = Query(type='outfit')
        if ignore_case:
            q.add_filter(field='name_lower', value=name.lower())
        else:
            q.add_filter(field='name', value=name)

        d = q.get_single()
        if len(d) == 0:
            return  # TODO: Replace with exception

        # Retrieve and return the object
        instance = Outfit.get(id=d['outfit_id'], data=d)
        return instance

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.alias = d.get('alias')
        self._leader_id = d['leader_character_id']
        self.member_count = d['member_count']
        self.name = d['name']
        self.date_created = datetime.utcfromtimestamp(int(d['time_created']))


class OutfitMember(CachableDataType):
    """An outfit member.

    An outfit member is the linking entity between an outfit and a player and
    contains information about their rank in the outfit and the date and time
    they joined.

    """

    _collection = 'outfit_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._character_id = None
        self.date_joined = None
        self.rank_name = None
        self.rank_ordinal = None

    # Define properties
    @property
    def character(self):
        try:
            return self._character
        except AttributeError:
            self._character = Character.get(id=self._character_id)
            return self._character

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self._character_id = d['character_id']
        self.date_joined = datetime.utcfromtimestamp(int(d['member_since']))
        self.rank_name = d['rank']
        self.rank_ordinal = d['rank_ordinal']
