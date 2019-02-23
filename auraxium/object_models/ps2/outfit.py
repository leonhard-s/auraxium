"""Defines outfit-related data types for PlanetSide 2."""

from datetime import datetime

from ...base_api import Query
from ..datatypes import DataType
from .character import Character
from ..exceptions import NoMatchesFoundError


class Outfit(DataType):
    """Represents a PS2 outfit.

    An outfit is a group of players. The individual player information needs to be resolved further.

    """

    _collection = 'outfit'

    def __init__(self, id_):
        self.id_ = id_

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
        """The leader of the outfit."""
        return Character.get(id_=self._leader_id)

    @property
    def members(self):
        """A list of characters that are part of this outfit."""
        try:
            return self._members
        except AttributeError:
            data = Query(collection='outfit_member', outfit_id=self.id_).get()
            self._members = OutfitMember.list(ids=[i['character_id'] for i in data])
            return self._members

    @staticmethod
    def get_by_name(name, ignore_case=True):
        """Retrieves an outfit by name."""
        # Generate request
        query = Query(collection='outfit')
        if ignore_case:
            query.add_term(field='name_lower', value=name.lower())
        else:
            query.add_term(field='name', value=name)
        data = query.get(single=True)
        if not data:
            raise NoMatchesFoundError

        # Retrieve and return the object
        instance = Outfit.get(id_=data['outfit_id'], data=data)
        return instance

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.alias = data_dict.get('alias')
        self._leader_id = data_dict['leader_character_id']
        self.member_count = data_dict['member_count']
        self.name = data_dict['name']
        self.date_created = datetime.utcfromtimestamp(int(data_dict['time_created']))


class OutfitMember(DataType):
    """An outfit member.

    An outfit member is the linking entity between an outfit and a player and
    contains information about their rank in the outfit and the date and time
    they joined.

    """

    _collection = 'outfit_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._character_id = None
        self.date_joined = None
        self.rank_name = None
        self.rank_ordinal = None

    # Define properties
    @property
    def character(self):
        """The character for this outfit member."""
        return Character.get(id_=self._character_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._character_id = data_dict['character_id']
        self.date_joined = datetime.utcfromtimestamp(int(data_dict['member_since']))
        self.rank_name = data_dict['rank']
        self.rank_ordinal = data_dict['rank_ordinal']
