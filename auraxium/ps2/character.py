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

    def __init__(self, id, populate=True):
        self.id = id  # character_id
        data = super(Character, self).get_data(self)

        self.asp = data.get('prestige_level')
        self.battle_rank = data.get('battle_rank')['value']
        self.battle_rank_progress_to_next = data.get('battle_rank')[
            'percent_to_next']
        self.certs_available = data.get('certs')['available_points']
        self.certs_earned = data.get('certs')['earned_points']
        self.certs_gifted = data.get('certs')['gifted_points']
        self.certs_spent = data.get('certs')['spent_points']
        self.certs_progress_to_next = data.get('certs')['percent_to_next']
        self.name = data.get('name')['first']
        self.faction = Faction(data.get('faction_id'))
        self.head = Head(data.get('head_id'))
        self.title = Title(data.get('title_id')) if data.get(
            'title_id') != '0' else None
        self.time_created = datetime.utcfromtimestamp(int(
            data.get('times')['creation']))
        self.time_last_saved = datetime.utcfromtimestamp(int(
            data.get('times')['last_save']))
        self.time_last_login = datetime.utcfromtimestamp(int(
            data.get('times')['last_login']))
        self.login_count = data.get('times')['login_count']
        self.minutes_played = data.get('times')['minutes_played']
        self.profile = Profile(data.get('profile_id'))
        self.daily_ribbon_count = data.get('daily_ribbon')['count']
        self.daily_ribbon_time = datetime.utcfromtimestamp(int(
            data.get('daily_ribbon')['time']))

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

        # Hard-coded head names and icons
        head_names = ['Caucasian Male', 'African Male', 'Hispanic Male',
                      'Asian Male', 'Caucasian Female', 'African Female',
                      'Hispanic Female', 'Asian Female']
        head_image_ids = [1177, 1173, 1179, 1175, 1176, 1172, 1178, 1174]
        self.image = Image(head_image_ids[int(id) - 1])
        self.name = head_names[int(id) - 1]
