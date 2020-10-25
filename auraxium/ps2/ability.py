"""Ability and ability type class definitions."""

from ..base import Cached
from ..census import Query
from ..models import AbilityData, AbilityTypeData, ResourceTypeData
from ..proxy import InstanceProxy


class ResourceType(Cached, cache_size=50, cache_ttu=3600.0):
    """A type of resource consumed by an ability."""

    collection = 'resource_type'
    data: ResourceTypeData
    dataclass = ResourceTypeData
    id_field = 'resource_type_id'

    @property
    def description(self) -> str:
        """A description of what this resource type is used for."""
        return self.data.description


class AbilityType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of ability.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'ability_type'
    data: AbilityTypeData
    dataclass = AbilityTypeData
    id_field = 'ability_type_id'


class Ability(Cached, cache_size=10, cache_ttu=60.0):
    """An ability cast by a character.

    Access the corresponding :class:`auraxium.ps2.ability.AbilityType`
    instance via the :meth:`type` method for information on generic
    parameters.
    """

    collection = 'ability'
    data: AbilityData
    dataclass = AbilityData
    id_field = 'ability_id'

    def resource_type(self) -> InstanceProxy[ResourceType]:
        """Return the resource type used by this ability, if any."""
        type_id = self.data.resource_type_id or -1
        query = Query(
            ResourceType.collection, service_id=self._client.service_id)
        query.add_term(field=ResourceType.id_field, value=type_id)
        return InstanceProxy(ResourceType, query, client=self._client)

    def type(self) -> InstanceProxy[AbilityType]:
        """Return the ability type of this ability."""
        query = Query(
            AbilityType.collection, service_id=self._client.service_id)
        query.add_term(
            field=AbilityType.id_field, value=self.data.ability_type_id)
        return InstanceProxy(AbilityType, query, client=self._client)
