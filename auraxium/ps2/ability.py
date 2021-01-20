"""Ability and ability type class definitions."""

from typing import Optional

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

    # Type hints for data class fallback attributes
    resource_type_id: int
    description: str


class AbilityType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of ability.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'ability_type'
    data: AbilityTypeData
    dataclass = AbilityTypeData
    id_field = 'ability_type_id'

    # Type hints for data class fallback attributes
    ability_type_id: int
    description: Optional[str]
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]
    param14: Optional[str]
    string1: Optional[str]
    string2: Optional[str]
    string3: Optional[str]
    string4: Optional[str]


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

    # Type hints for data class fallback attributes
    ability_id: int
    ability_type_id: int
    expire_msec: Optional[int]
    first_use_delay_msec: Optional[int]
    next_use_delay_msec: Optional[int]
    reuse_delay_msec: Optional[int]
    resource_type_id: Optional[int]
    resource_first_cost: Optional[int]
    resource_cost_per_msec: Optional[int]
    distance_max: Optional[float]
    radius_max: Optional[float]
    flag_toggle: Optional[bool]
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]
    param6: Optional[str]
    param7: Optional[str]
    param8: Optional[str]
    param9: Optional[str]
    param10: Optional[str]
    param11: Optional[str]
    param12: Optional[str]
    param13: Optional[str]
    param14: Optional[str]
    string1: Optional[str]
    string2: Optional[str]
    string3: Optional[str]
    string4: Optional[str]

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
