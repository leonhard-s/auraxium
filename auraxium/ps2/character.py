from datetime import datetime

from ..census import Query
from ..datatypes import DynamicDatatype


class Character(DynamicDatatype):
    """A PlanetSide 2 Character.

    Can be directly queried by "id" or "name".
    """

    _collection = 'character'

    def __init__(self, id, populate=True):
        self.id = id  # character_id

        self.asp = None
        self.battle_rank = None
        self.battle_rank_percent_to_next = None

        self.certs_available = None
        self.certs_earned = None
        self.certs_gifted = None
        self.certs_spent = None
        self.certs_percent_to_next = None

        self.name = None
        self.faction = None

        self.head = None
        self.title = None

        self.time_created = None
        self.time_last_seen = None
        self.time_last_login = None
        self.login_count = None
        self.minutes_played = None

        self.profile = None

        self.daily_ribbon_count = None
        self.daily_ribbon_time = None

        # Populate character
        q = Query(self).add_filter('character_id', id)
        q.hide('character_id', 'name.first_lower',
               'times.creation_date', 'times.last_save_date',
               'times.last_login_date', 'daily_ribbon.date')
        data = q.get_single()

        self.asp = int(data['prestige_level'])  # ASP level / prestige level
        self.battle_rank = int(data['battle_rank']['value'])
        self.battle_rank_progress_to_next = float(
            data['battle_rank']['percent_to_next'])
        self.certs_available = int(data['certs']['available_points'])
        self.certs_earned = int(data['certs']['earned_points'])
        self.certs_gifted = int(data['certs']['gifted_points'])
        self.certs_spent = int(data['certs']['spent_points'])
        self.certs_progress_to_next = float(data['certs']['percent_to_next'])
        self.name = data['name']['first']  # name.first
        # self.faction =   # faction_id
        # self.head = None  # head_id
        # self.title = None  # title_id # NOTE: MAKE DYNAMIC?
        self.time_created = datetime.utcfromtimestamp(int(
            data['times']['creation']))
        self.time_last_seen = datetime.utcfromtimestamp(int(
            data['times']['last_save']))
        self.time_last_login = datetime.utcfromtimestamp(int(
            data['times']['last_login']))
        self.login_count = int(data['times']['login_count'])
        self.minutes_played = int(data['times']['minutes_played'])
        # self.profile = None  # profile_id
        self.daily_ribbon_count = int(data['daily_ribbon']['count'])
        self.daily_ribbon_time = datetime.utcfromtimestamp(int(
            data['daily_ribbon']['time']))

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


class Head(DynamicDatatype):
    def __init__(self):
        pass
