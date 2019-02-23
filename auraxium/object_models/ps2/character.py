from datetime import datetime

from ...base_api import Query
from ..datatypes import DataType
from .currency import Currency
from .faction import Faction
from .image import Image
from .profile import Profile
from .title import Title
from .world import World
from ..exceptions import NoMatchesFoundError


class Character(DataType):
    """A PlanetSide 2 character.

    Characters are players, as well as the owners of items.

    """

    _collection = 'character'

    # Missing related collections:
    #     achievements
    #     directive
    #     directive_objective
    #     directive_tier
    #     directive_tree
    #     event
    #     event_grouped
    #     friends
    #     items
    #     leaderboard
    #     online_status
    #     skill
    #     stat
    #     stat_by_faction
    #     stat_history
    #     weapon_stat
    #     weapon_stat_by_faction

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.asp_rank = None
        self.battle_rank = None
        self.battle_rank_percent = None
        self.certs_available = None
        self.certs_earned = None
        self.certs_gifted = None
        self.certs_spent = None
        self.cert_percent = None
        self._currency = None  # Internal (See properties)
        self.daily_ribbon_bonus_count = None
        self.daily_ribbon_bonus_last = None
        self._faction_id = None
        self.login_count = None
        self._head_id = None
        self.play_time = None
        self.name = None
        self._profile_id = None
        self._profiles = None  # Internal (See properties)
        self.time_created = None
        self.time_last_saved = None
        self.time_last_login = None
        self._title_id = None
        self._world = None  # Internal (See properties)

    # Define properties
    @property
    def currency(self):
        try:
            return self._currency
        except AttributeError:
            data = Query(collection='characters_currency', character_id=self.id_).get()
            self._currency = Currency.list(ids=[c['currency_id'] for c in data])
            return self._currency

    @property
    def faction(self):
        return Faction.get(id_=self._faction_id)

    @staticmethod
    def get_by_name(name, ignore_case=True):
        # Generate request
        query = Query(collection='character')
        if ignore_case:
            query.add_term(field='name.first_lower', value=name.lower())
        else:
            query.add_term(field='name.first', value=name)
        data = query.get(single=True)
        if not data:
            raise NoMatchesFoundError
        # Retrieve and return the object
        instance = Character.get(id_=data['character_id'], data=data)
        return instance

    @property
    def head(self):
        return Head(id_=self._head_id)

    @property
    def profile(self):
        return Profile.get(id_=self._profile_id)

    @property
    def title(self):
        return Title.get(id_=self._title_id)

    @property
    def world(self):
        try:
            return self._world
        except AttributeError:
            data = Query(collection='characters_world', character_id=self.id_).get(single=True)
            self._world = World.get(id_=data['world_id'])
            return self._world

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.asp_rank = d['prestige_level']
        self.battle_rank = d['battle_rank']['value']
        self.battle_rank_percent = d['battle_rank']['percent_to_next']
        self.certs_available = d['certs']['available_points']
        self.certs_earned = d['certs']['earned_points']
        self.certs_gifted = d['certs']['gifted_points']
        self.certs_spent = d['certs']['spent_points']
        self.cert_percent = d['certs']['percent_to_next']
        self.daily_ribbon_bonus_count = d['daily_ribbon']['count']
        self.daily_ribbon_bonus_last = datetime.utcfromtimestamp(int(
            d['daily_ribbon']['time']))
        self._faction_id = d['faction_id']
        self.login_count = d['times']['login_count']
        self._head_id = d['head_id']
        self.play_time = float(d['times']['minutes_played']) / 60.0
        self.name = d['name']['first']
        self._profile_id = d['profile_id']
        self.time_created = datetime.utcfromtimestamp(int(
            d['times']['creation']))
        self.time_last_saved = datetime.utcfromtimestamp(int(
            d['times']['last_save']))
        self.time_last_login = datetime.utcfromtimestamp(int(
            d['times']['last_login']))
        self._title_id = d.get('title_id')


class Head():
    """A head model a character can have.

    Head models are not an explicit colletion in the API, so most attributes
    have to be hard-coded to allow for display of player busts or icons.

    """

    def __init__(self, id_):
        self.id_ = id_

        # Hard-coded head names and icons
        head_image_ids = [1177, 1173, 1179, 1175, 1176, 1172, 1178, 1174]
        head_names = ['Caucasian Male', 'African Male', 'Hispanic Male',
                      'Asian Male', 'Caucasian Female', 'African Female',
                      'Hispanic Female', 'Asian Female']

        # Set attribute values
        self._image_id = head_image_ids[int(id_) - 1]
        self.name = head_names[int(id_) - 1]

    # Define properties
    @property
    def image(self):
        return Image.get(id_=self._image_id)
