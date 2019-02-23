"""Defines alert-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from ..misc import LocalizedString


class Alert(DataType, NamedDataType):
    """An alert/event.

    An alert that can take place on Auraxis. Not all event types are
    currently enabled in-game.

    """

    _collection = 'metagame_event'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self.experience_bonus = None
        self.name = None
        self.type = None

    def populate(self, data=None):
        """Populates the data type."""
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict['description'])
        self.experience_bonus = data_dict['experience_bonus']
        self.name = LocalizedString(data_dict['name'])
        # Hard-coded descriptions of the base alert types, 1 and 6 are unused.
        alert_types = {'1': 'Territory Control', '2': 'Facility Type',
                       '5': 'Warpgates Stabilizing', '6': 'Conquest',
                       '8': 'Meltdown', '9': 'Unstable Meltdown',
                       '10': 'Aerial Anomalies'}
        self.type = alert_types[data_dict['type']]


class AlertState(DataType):
    """The state of an alert.

    Lists the states an alert can be in, like "started".

    """

    _collection = 'metagame_event_state'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.name = None

    def populate(self, data=None):
        """Populates the data type."""
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.name = data_dict['name']
