"""Ability and ability type class definitions."""

from typing import Optional

from ..base import Cached
from ..census import Query
from ..models import AbilityData, AbilityTypeData, ResourceTypeData
from .._proxy import InstanceProxy

__all__ = [
    'Ability',
    'AbilityData',
    'AbilityType',
    'ResourceType'
]


class ResourceType(Cached, cache_size=50, cache_ttu=3600.0):
    """A type of resource consumed by an ability.

    .. attribute:: id
       :type: int

       The unique ID of this resource type.

    .. attribute:: description
       :type: str

       A description of what this resource type is used for.
    """

    collection = 'resource_type'
    data: ResourceTypeData
    id_field = 'resource_type_id'
    _model = ResourceTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str


class AbilityType(Cached, cache_size=20, cache_ttu=60.0):
    """A type of ability.

    This class mostly specifies the purpose of any generic parameters.

    .. attribute:: id
       :type: int

       The unique ID for this ability type.

    .. attribute:: description
       :type: str | None

       A description of what this ability type is used for.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       abilities of this type.

    .. attribute:: string*
       :type: str | None

       Descriptions of what the corresponding string value is used for
       in abilities of this type.
    """

    collection = 'ability_type'
    data: AbilityTypeData
    id_field = 'ability_type_id'
    _model = AbilityTypeData

    # Type hints for data class fallback attributes
    id: int
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

    Access the corresponding :class:`~auraxium.ps2.AbilityType`
    instance via the :meth:`Ability.type` method for information on
    generic parameters.

    .. attribute:: id
       :type: int

       The unique ID of this ability.

    .. attribute:: ability_type_id
       :type: int

       The associated ability type for this ability.

    .. attribute:: expire_msec
       :type: int | None

       The duration of the ability.

    .. attribute:: first_use_delay_msec
       :type: int | None

       The initial cooldown of the ability.

    .. attribute:: next_use_delay_msec
       :type: int | None

       The reuse cooldown of the ability.

    .. attribute:: resource_type_id
       :type: int | None

       The resource type used by the ability.

    .. attribute:: resource_first_cost
       :type: int | None

       The initial cast cost of the ability.

    .. attribute:: resource_cost_per_msec
       :type: int | None

       The resource cost per second for channeled abilities.

    .. attribute:: distance_max
       :type: float | None

       (Not yet documented)

    .. attribute:: radius_max
       :type: float | None

       (Not yet documented)

    .. attribute:: flag_toggle
       :type: bool | None

       Whether the ability is toggled.

    .. attribute:: param*
       :type: str | None

       Type-specific parameters for this ability. Refer to the
       corresponding :class:`~auraxium.ps2.AbilityType` for details.

    .. attribute:: string*
       :type: str | None

       Type-specific string values for this ability. Refer to the
       corresponding :class:`~auraxium.ps2.AbilityType` for details.
    """

    collection = 'ability'
    data: AbilityData
    id_field = 'ability_id'
    _model = AbilityData

    # Type hints for data class fallback attributes
    id: int
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
