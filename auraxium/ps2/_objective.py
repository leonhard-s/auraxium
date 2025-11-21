"""Objective class definitions."""

from typing import Final
from ..base import Cached
from ..census import Query
from ..models import ObjectiveData, ObjectiveTypeData
from .._rest import RequestClient
from .._proxy import InstanceProxy, SequenceProxy

__all__ = [
    'Objective',
    'ObjectiveType'
]


class ObjectiveType(Cached, cache_size=10, cache_ttu=60.0):
    """A type of objective.

    This class mostly specifies the purpose of any generic parameters.

    .. attribute:: id
       :type: int

       The unique ID of the objective type. In the API payload, this
       field is called ``objective_type_id``.

    .. attribute:: description
       :type: str

       A description of what the objective type is used for.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       objectives of this type.
    """

    collection = 'objective_type'
    data: ObjectiveTypeData
    id_field = 'objective_type_id'
    _model = ObjectiveTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None


class Objective(Cached, cache_size=10, cache_ttu=60.0):
    """A objective presented to a character.

    .. attribute:: id
       :type: int

       The unique ID of this objective. In the API payload, this
       field is called ``objective_id``.

    .. attribute:: objective_type_id
       :type: int

       The associated :class:`ObjectiveType` for this objective.

       .. seealso::

          :meth:`type` -- The type of objective.

    .. attribute:: objective_group_id
       :type: int

       The objective group this objective contributes to. Used to link
       objectives to directives.

       .. seealso::

          :meth:`get_by_objective_group` -- Get the list of objectives
          for a given objective group.

    .. attribute:: param*
       :type: str | None

       Type-specific parameters for this objective. Refer to the
       corresponding :class:`~auraxium.ps2.ObjectiveType` for
       details.
    """

    collection = 'objective'
    data: ObjectiveData
    id_field = 'objective_id'
    _model = ObjectiveData

    # Type hints for data class fallback attributes
    id: int
    objective_type_id: int
    objective_group_id: int
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None

    @classmethod
    def get_by_objective_group(
            cls, objective_group_id: int,
            client: RequestClient) -> SequenceProxy['Objective']:
        """Return any rewards contained from the given reward group.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(Objective.collection, service_id=client.service_id,
                      objective_group_id=objective_group_id)
        query.limit(1000)
        return SequenceProxy(Objective, query, client=client)

    @classmethod
    def get_by_objective_set(
            cls, objective_set_id: int,
            client: RequestClient) -> SequenceProxy['Objective']:
        """Return any rewards contained in the given reward set.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'objective_set_to_objective'
        query = Query(collection, service_id=client.service_id,
                      objective_set_id=objective_set_id)
        query.limit(1000)
        join = query.create_join(Objective.collection)
        join.set_fields('objective_group_id').set_list(True)
        return SequenceProxy(Objective, query, client=client)

    def type(self) -> InstanceProxy[ObjectiveType]:
        """Return the objective type of this objective.

         This returns an :class:`auraxium.InstanceProxy`.
         """
        query = Query(
            ObjectiveType.collection, service_id=self._client.service_id)
        query.add_term(
            field=ObjectiveType.id_field, value=self.data.objective_type_id)
        return InstanceProxy(ObjectiveType, query, client=self._client)
