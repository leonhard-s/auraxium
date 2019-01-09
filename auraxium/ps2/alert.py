from ..census import Query
from ..datatypes import StaticDatatype


class AlertState(StaticDatatype):
    _collection = 'metagame_event_state'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.name = data['name']


class AlertType(StaticDatatype):
    _collection = 'metagame_event'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()
        self.description = data['description'][next(iter(data['description']))]
        self.experience_bonus = int(data['experience_bonus'])
        self.name = data['name'][next(iter(data['name']))]

        # Hard-coded descriptions of the base alert types
        # 1 and 6 are currently unused.
        base_alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                            '5': 'Warpgates Stabilizing', '6': 'Conquest',
                            '8': 'Meltdown', '9': 'Unstable Meltdown',
                            '10': 'Aerial Anomalies'}

        self.type = base_alert_types[data['type']]
