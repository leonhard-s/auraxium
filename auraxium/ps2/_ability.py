"""Ability and ability type class definitions."""

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
    """Resources are entity-specific states used by other mechanics.

    You can think of them as attributes attached to a character or
    vehicle that is then modified by other game mechanics.

    This includes active class abilities like the Combat Medic's Nano
    Regen Device or the Heavy Assault's overshield, physical resources
    like Cortium carried by A.N.T.s or Collossi, but are also used as
    a reservoir for other game mechanics like Esamir's Electrical Storm
    vehicle debuff.

    .. attribute:: id
       :type: int

       The unique ID of this resource type. In the API payload, this
       field is called ``resource_type_id``.

    .. attribute:: description
       :type: str

       An internal description of what this resource type is used for.
       This string is not safe to display to users as this field could
       be blank or set to a dummy value like
       ``Esamir.Storm.VehicleOverload``.
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

    Ability types specify the basic function of a given
    :class:`Ability`. The ``param*`` fields in the ability type list
    what these generic parameters are used for in the corresponding
    abilities (where specified).

    .. note::

       The purpose of these base types and what mechanics they
       correspond to in-game is currently undocumented due to the lack
       of links between abilities and other types in the API.

       More information needed & much appreciated.

    .. attribute:: id
       :type: int

       The unique ID for this ability type. In the API payload, this
       field is called ``ability_type_id``.

    .. attribute:: description
       :type: str | None

       A description of what this ability type is used for.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       abilities of this type.

       .. note::

          As of April 2021, only the ``param1`` field is used.

    .. attribute:: string*
       :type: str | None

       Descriptions of what the corresponding string value is used for
       in abilities of this type.

       .. note::

          As of April 2021, none of the string fields are used.
    """

    collection = 'ability_type'
    data: AbilityTypeData
    id_field = 'ability_type_id'
    _model = AbilityTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str | None
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None
    param14: str | None
    string1: str | None
    string2: str | None
    string3: str | None
    string4: str | None


class Ability(Cached, cache_size=10, cache_ttu=60.0):
    """An ability triggered by a character or vehicle.

    See the corresponding :class:`~auraxium.ps2.AbilityType` instance
    via the :meth:`Ability.type` method for information on generic
    parameters.

    .. note::

       The in-game mechanics these abilities correspond to is currently
       undocumented due to the lack of links between abilities and
       other types in the API.

       It should be possible to correlate fields like
       :attr:`expire_msec` or :attr:`reuse_delay_msec` to their
       corresponding in-game ability. Though very time-consuming.

       More information needed & much appreciated.

    .. attribute:: id
       :type: int

       The unique ID of this ability. In the API payload, this
       field is called ``ability_id``.

    .. attribute:: ability_type_id
       :type: int

       The ID of the :class:`AbilityType` of this ability.

       .. seealso::

          :meth:`type` -- Return the type of this ability.

    .. attribute:: expire_msec
       :type: int | None

       The duration of a single-shot ability in milliseconds.

       Only present for ability types 3, 6, 12, 16, 17, and 30.

    .. attribute:: first_use_delay_msec
       :type: int | None

       The initial delay before the ability can be used in
       milliseconds.

       .. note::

          As of April 2021, this field is always 0 or 1 for all fields.
          Since an initial cast delay of 1 millisecond makes little
          sense, this field is likely unused.

    .. attribute:: next_use_delay_msec
       :type: int | None

       The cooldown of a single-shot ability in milliseconds.

       .. note::

          The difference between this field and
          :attr:`reuse_delay_msec` has not been tested yet.

       Only present for ability types 6, 13, and 30.

    .. attribute:: reuse_delay_msec
       :type: int | None

       The recharge cooldown for multi-use abilities in milliseconds.

       .. note::

          The difference between this field and
          :attr:`next_use_delay_msec` has not been tested yet.

       Only present for ability types 3, 6, 12, 16, 17, and 30.

    .. attribute:: resource_type_id
       :type: int | None

       The ID of the :class:`ResourceType` used by this ability.

       Only present for ability types 3, 6, 10, 13, and 30.

       .. seealso::

          :meth:`resource_type` -- Return the resource type of this
          ability.

    .. attribute:: resource_first_cost
       :type: int | None

       The initial cost of activating a continuous the ability.

       Only present for ability types 3, 6, 10, 13, and 30.

    .. attribute:: resource_cost_per_msec
       :type: int | None

       Only present for ability types 3, 6, 10, 13, and 30.

       The amount drained from the ability's :class:`ResourceType`
       every millisecond as long as the ability is active.

    .. attribute:: distance_max
       :type: float | None

       Not yet documented. See also :attr:`radius_max`.

    .. attribute:: radius_max
       :type: float | None

       Not yet documented. See also :attr:`distance_max`.

    .. attribute:: flag_toggle
       :type: bool | None

       Whether the ability is channeled and can be toggled on and off.

       Only present for ability types 3, 6, 10, 13, and 30.

    .. attribute:: param*
       :type: str | None

       Type-specific parameters for this ability. Refer to the
       corresponding :class:`AbilityType` for details.

       .. note::

          As of April 2021, only the ``param1`` field is used.

    .. attribute:: string*
       :type: str | None

       Type-specific string values for this ability. Refer to the
       corresponding :class:`AbilityType` for details.

       .. note::

          As of April 2021, none of the string fields are used.
    """

    collection = 'ability'
    data: AbilityData
    id_field = 'ability_id'
    _model = AbilityData

    # Type hints for data class fallback attributes
    id: int
    ability_type_id: int
    expire_msec: int | None
    first_use_delay_msec: int | None
    next_use_delay_msec: int | None
    reuse_delay_msec: int | None
    resource_type_id: int | None
    resource_first_cost: int | None
    resource_cost_per_msec: int | None
    distance_max: float | None
    radius_max: float | None
    flag_toggle: bool | None
    param1: str | None
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None
    param6: str | None
    param7: str | None
    param8: str | None
    param9: str | None
    param10: str | None
    param11: str | None
    param12: str | None
    param13: str | None
    param14: str | None
    string1: str | None
    string2: str | None
    string3: str | None
    string4: str | None

    def resource_type(self) -> InstanceProxy[ResourceType]:
        """Return the resource type used by this ability, if any.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        type_id = self.data.resource_type_id or -1
        query = Query(
            ResourceType.collection, service_id=self._client.service_id)
        query.add_term(field=ResourceType.id_field, value=type_id)
        return InstanceProxy(ResourceType, query, client=self._client)

    def type(self) -> InstanceProxy[AbilityType]:
        """Return the ability type of this ability.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            AbilityType.collection, service_id=self._client.service_id)
        query.add_term(
            field=AbilityType.id_field, value=self.data.ability_type_id)
        return InstanceProxy(AbilityType, query, client=self._client)
