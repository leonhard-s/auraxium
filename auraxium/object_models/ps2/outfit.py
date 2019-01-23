from datetime import datetime

from ...base_api import Query
from ..datatypes import CachableDataType
from .character import Character
from ..exceptions import NoMatchesFoundError


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
        self._members = None  # Internal (See properties)
        self.name = None
        self.date_created = None

    # Define properties
    @property
    def leader(self):
        return Character.get(id=self._leader_id)

    @property
    def members(self):
        try:
            return self._members
        except AttributeError:
            data = Query(collection='outfit_member', outfit_id=self.id).get()
            self._members = OutfitMember.list(ids=[i['character_id'] for i in data])
            return self._members

    @staticmethod
    def get_by_name(name, ignore_case=True):
        # Generate request
        q = Query(collection='outfit')
        if ignore_case:
            q.add_term(field='name_lower', value=name.lower())
        else:
            q.add_term(field='name', value=name)
        data = q.get(single=True)
        if not data:
            raise NoMatchesFoundError

        # Retrieve and return the object
        instance = Outfit.get(id=data['outfit_id'], data=data)
        return instance

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

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
        return Character.get(id=self._character_id)

    def _populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._character_id = d['character_id']
        self.date_joined = datetime.utcfromtimestamp(int(d['member_since']))
        self.rank_name = d['rank']
        self.rank_ordinal = d['rank_ordinal']
