from typing import List

from ..datatypes import DataType
from ..typing import Param


class Objective(DataType):
    """An objective.

    An objective to be completed. Links with ObjectiveSet fields are still
    untested.

    """

    _collection = 'objective'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.objective_group_id = None
        self._objective_type_id = None

        self.param: List[Param] = [None for i in range(13)]

    # Define properties
    @property
    def objective_type(self):
        return ObjectiveType.get(id_=self._objective_type_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.objective_group_id = d.get('objective_group_id')
        self._objective_type_id = d['objective_type_id']

        self.param = [d['param' + str(i + 1)] if d.get('param' + str(i + 1))
                      is not None else None for i in range(13)]


class ObjectiveType(DataType):
    """An objective type.

    The type of objective for a given objective. Contains information about
    the purpose of the "param" attributes.

    """

    _collection = 'objective_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

        self.param: List[Param] = [None for i in range(13)]

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d['description']

        self.param = [d['param' + str(i + 1)] if d.get('param' + str(i + 1))
                      is not None else None for i in range(13)]
