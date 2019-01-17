from ..census import Query
from ..datatypes import EnumeratedDataType, NamedDataType
from ..misc import LocalizedString


class Alert(EnumeratedDataType, NamedDataType):
    """An alert/event.

    An alert that can take place on Auraxis. Not all event types are
    currently enabled in-game.

    """

    _collection = 'metagame_event'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self.experience_bonus = None
        self.name = None
        self.type = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self.experience_bonus = d['experience_bonus']
        self.name = LocalizedString(d['name'])
        # Hard-coded descriptions of the base alert types, 1 and 6 are unused.
        alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                            '5': 'Warpgates Stabilizing', '6': 'Conquest',
                            '8': 'Meltdown', '9': 'Unstable Meltdown',
                            '10': 'Aerial Anomalies'}
        self.type = alert_types[d['type']]


class AlertState(EnumeratedDataType):
    """The state of an alert.

    Lists the states an alert can be in, like "started".

    """

    _collection = 'metagame_event_state'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.name = d['name']
