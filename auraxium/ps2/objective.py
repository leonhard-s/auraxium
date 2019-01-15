from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from .objective import ObjectiveType


class Objective(CachableDataType):
    """An objective.

    An objective to be completed. Links with ObjectiveSet fields are still
    untested.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.objective_group_id = None
        self._objective_type_id = None
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

        # Define properties
        @property
        def objective_type(self):
            try:
                return self._objective_type
            except AttributeError:
                self._objective_type = ObjectiveType.get(
                    id=self._objective_type_id)
                return self._objective_type

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.objective_group_id = data.get('objective_group_id')
        self._objective_type_id = data['objective_type_id']
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = data.get(\'param{0}\')\n'.format(i + 1)
        exec(s)


class ObjectiveType(EnumeratedDataType):
    """An objective type.

    The type of objective for a given objective. Contains information about
    the purpose of the "param" attributes.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    def _populate(self, data_override=None):
        data = data_override if data_override != None else super().get(self.id)

        # Set attribute values
        self.description = data['description']
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = data.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
