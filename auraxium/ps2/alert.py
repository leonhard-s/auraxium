from ..census import Query
from ..datatypes import EnumeratedDataType
from ..misc import LocalizedString


class AlertState(EnumeratedDataType):
    """The state of an alert.

    Lists the states an alert can be in, like "started".

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.name = None

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.name = data['name']


class Alert(EnumeratedDataType):
    """An alert/event.

    An alert that can take place on Auraxis. Not all event types are
    currently enabled in-game.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self.experience_bonus = None
        self.name = None
        self.type = None

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.description = LocalizedString(data['description'])
        self.experience_bonus = data['experience_bonus']
        self.name = LocalizedString(data['name'])
        # Hard-coded descriptions of the base alert types, 1 and 6 are unused.
        alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                            '5': 'Warpgates Stabilizing', '6': 'Conquest',
                            '8': 'Meltdown', '9': 'Unstable Meltdown',
                            '10': 'Aerial Anomalies'}
        self.type = alert_types[data['type']]
