from datetime import datetime

from ..census import Query
from ..datatypes import CachableDataType
from .currency import Currency
from .faction import Faction
from .image import Image
from .profile import Profile
from .title import Title


class Character(CachableDataType):
    """A PlanetSide 2 character.

    Characters are players, as well as the owners of items.

    """

    # Missing related collections:
    #     achievements
    #     directive
    #     directive_objective
    #     directive_tier
    #     directive_tree
    #     event
    #     event_grouped
    #     items
    #     leaderboard
    #     skill
    #     stat
    #     stat_by_faction
    #     stat_history
    #     weapon_stat
    #     weapon_stat_by_faction

    def __init__(self, id):
        self.id = id

        # Set default values
        self.asp_rank = None
        self.battle_rank = None
        self.battle_rank_percent = None
        self.certs_available = None
        self.certs_earned = None
        self.certs_gifted = None
        self.certs_spent = None
        self.cert_percent = None
        self.daily_ribbon_bonus_count = None
        self.daily_ribbon_bonus_last = None
        self._faction_id = None
        self.login_count = None
        self._head_id = None
        self.play_time = None
        self.name = None
        self._profile_id = None
        self.time_created = None
        self.time_last_saved = None
        self.time_last_login = None
        self._title_id = None

        # Define properties
        @property
        def currency(self):
            try:
                return self._currency
            except AttributeError:
                q = Query(type='characters_currency')
                data = q.add_filter(field='character_id', value=self.id).get()
                self._currency = Currency.list(
                    [c['currency_id'] for c in data])
                return self._currency

        @property
        def faction(self):
            try:
                return self._faction
            except AttributeError:
                self._faction = Faction.get(id=self._faction_id)
                return self._faction

        @property
        def friends(self):
            try:
                return self._world
            except AttributeError:
                q = Query(type='item_profile')
                data = q.add_filter(field='item_id', value=self.id).get()
                self._profiles = Profile.list([i['profile_id'] for i in data])
                return self._profiles

        @property
        def head(self):
            try:
                return self._head
            except AttributeError:
                self._head = Head(id=self._head_id)
                return self._head

        @property
        def online_status(self):
            q = Query(type='characters_online_status')
            q.add_filter(field='character_id', value=self.id)
            data =
            return data['online_status']

        @property
        def profile(self):
            try:
                return self._profile
            except AttributeError:
                self._profile = Profile.get(id=self._profile_id)
                return self._profile

        @property
        def title(self):
            try:
                return self._title
            except AttributeError:
                self._title = Title.get(id=self._title_id)
                return self._title

        @property
        def world(self):
            try:
                return self._world
            except AttributeError:
                q = Query(type='characters_world')
                q.add_filter(field='character_id', value=self.id)
                data = q.get_single()
                self._world = World.get(data['world_id'])
                return self._world

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.asp_rank = data['prestige_level']
        self.battle_rank = data['battle_rank']['value']
        self.battle_rank_percent = data['battle_rank']['percent_to_next']
        self.certs_available = data['certs']['available_points']
        self.certs_earned = data['certs']['earned_points']
        self.certs_gifted = data['certs']['gifted_points']
        self.certs_spent = data['certs']['spent_points']
        self.cert_percent = data['certs']['percent_to_next']
        self.daily_ribbon_bonus_count = data['daily_ribbon']['count']
        self.daily_ribbon_bonus_last = datetime.utcfromtimestamp(int(
            data['daily_ribbon']['time']))
        self._faction_id = data['faction_id']
        self.login_count = data['times']['login_count']
        self._head_id = data['head_id']
        self.play_time = data['times']['minutes_played'] / 60.0
        self.name = data['name']['first']
        self._profile_id = data['profile_id']
        self.time_created = datetime.utcfromtimestamp(int(
            data['times']['creation']))
        self.time_last_saved = datetime.utcfromtimestamp(int(
            data['times']['last_save']))
        self.time_last_login = datetime.utcfromtimestamp(int(
            data['times']['last_login']))
        self._title_id = data.get('title_id')


class Head(object):
    """A head model a character can have.

    Head models are not an explicit colletion in the API, so most attributes
    have to be hard-coded to allow for display of player busts or icons.

    """

    def __init__(self, id):
        self.id = id

        # Hard-coded head names and icons
        head_image_ids = [1177, 1173, 1179, 1175, 1176, 1172, 1178, 1174]
        head_names = ['Caucasian Male', 'African Male', 'Hispanic Male',
                      'Asian Male', 'Caucasian Female', 'African Female',
                      'Hispanic Female', 'Asian Female']

        # Set attribute values
        self._image_id = head_image_ids[int(id) - 1]
        self.name = head_names[int(id) - 1]

        # Define properties
        @property
        def image(self):
            try:
                return self._image
            except AttributeError:
                self._image = Image.get(id=self._image_id)
                return self._image
