from ..census import Query
from ..datatypes import StaticDatatype


class AlertState(StaticDatatype):
    _collection = 'metagame_event_state'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.name = data.get('name')

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'AlertState (ID: {}, Name: "{}")'.format(self.id, self.name)


class AlertType(StaticDatatype):
    _collection = 'metagame_event'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.experience_bonus = data.get('experience_bonus')
        self.name = data.get('name')

        # Hard-coded descriptions of the base alert types
        # 1 and 6 are currently unused.
        base_alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                            '5': 'Warpgates Stabilizing', '6': 'Conquest',
                            '8': 'Meltdown', '9': 'Unstable Meltdown',
                            '10': 'Aerial Anomalies'}

        self.type = base_alert_types[data.get('type')]

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'AlertType (ID: {}, Name[en]: "{}")'.format(
            self.id, self.name['en'])
