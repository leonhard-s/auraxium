from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType


class Objective(CachableDataType):
    """An objective.

    An objective to be completed. Links with ObjectiveSet fields are still
    untested.

    """

    _collection = 'objective'

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

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.objective_group_id = d.get('objective_group_id')
        self._objective_type_id = d['objective_type_id']
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)


class ObjectiveType(EnumeratedDataType):
    """An objective type.

    The type of objective for a given objective. Contains information about
    the purpose of the "param" attributes.

    """

    _collection = 'objective_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
