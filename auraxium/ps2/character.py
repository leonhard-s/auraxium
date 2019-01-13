from datetime import datetime

from ..census import Query
from ..datatypes import DynamicDatatype, StaticDatatype
from .faction import Faction
from .image import Image
from .profile import Profile
from .title import Title


class Character(DynamicDatatype):
    """A PlanetSide 2 character."""

    _collection = 'character'
    _join = ['faction', 'profile', 'title']

    def __init__(self, id, data_override=None):
        self.id = id

        data = data_override if data_override != None else super().get_data(self)

        self.asp = data.get('prestige_level')
        self.battle_rank = data.get('battle_rank')['value']
        self.battle_rank_progress_to_next = data.get('battle_rank')[
            'percent_to_next']
        self.certs_available = data.get('certs')['available_points']
        self.certs_earned = data.get('certs')['earned_points']
        self.certs_gifted = data.get('certs')['gifted_points']
        self.certs_spent = data.get('certs')['spent_points']
        self.certs_progress_to_next = data.get('certs')['percent_to_next']
        self.daily_ribbon_count = data.get('daily_ribbon')['count']
        self.daily_ribbon_time = datetime.utcfromtimestamp(int(
            data.get('daily_ribbon')['time']))
        self.faction = Faction(id=data.get('faction_id'),
                               data_override=data.get('faction'))
        self.login_count = data.get('times')['login_count']
        self.head = Head(data.get('head_id'))
        self.minutes_played = data.get('times')['minutes_played']
        self.name = data.get('name')['first']
        self.profile = Profile(id=data.get('profile_id'),
                               data_override=data.get('profile'))
        self.time_created = datetime.utcfromtimestamp(int(
            data.get('times')['creation']))
        self.time_last_saved = datetime.utcfromtimestamp(int(
            data.get('times')['last_save']))
        self.time_last_login = datetime.utcfromtimestamp(int(
            data.get('times')['last_login']))
        self.title = Title(id=data.get('title_id'), data_override=data.get(
            'title')) if data.get('title_id') != '0' else None

        @property
        def achievements(self):
            pass

        @property
        def currency(self):
            pass

        @property
        def directive(self):
            pass

        @property
        def directive_objective(self):
            pass

        @property
        def directive_tier(self):
            pass

        @property
        def directive_tree(self):
            pass

        @property
        def event(self):
            pass

        @property
        def event_grouped(self):
            pass

        @property
        def friends(self):
            pass

        @property
        def items(self):
            pass

        @property
        def leaderboard(self):
            pass

        @property
        def online_status(self):
            pass

        @property
        def skill(self):  # certification?
            pass

        @property
        def stat(self):
            pass

        @property
        def stat_by_faction(self):
            pass

        @property
        def stat_history(self):
            pass

        @property
        def weapon_stat(self):
            pass

        @property
        def weapon_stat_by_faction(self):
            pass

        @property
        def world(self):
            pass

    def __str__(self):
        return 'Character (ID: {}, Name: "{}")'.format(self.id, self.name)


class Head(StaticDatatype):
    """A head model a character can have.

    Head models are not an explicit colletion in the API, so most attributes
    have to be hard-coded to allow for display of player busts or icons.

    """

    def __init__(self, id):
        self.id = id

        if super().is_cached(self):
            return

        # Hard-coded head names and icons
        head_names = ['Caucasian Male', 'African Male', 'Hispanic Male',
                      'Asian Male', 'Caucasian Female', 'African Female',
                      'Hispanic Female', 'Asian Female']
        head_image_ids = [1177, 1173, 1179, 1175, 1176, 1172, 1178, 1174]
        self.image = Image(head_image_ids[int(id) - 1])
        self.name = head_names[int(id) - 1]

        super()._add_to_cache(self)  # Cache this instance for future use
