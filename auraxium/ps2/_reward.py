"""Reward and reward type class definitions."""

from typing import Final

from ..base import Cached
from ..census import Query
from ..models import RewardData, RewardTypeData
from .._rest import RequestClient
from .._proxy import InstanceProxy, SequenceProxy

__all__ = [
    'Reward',
    'RewardType'
]


class RewardType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of reward.

    This class mostly specifies the purpose of any generic parameters.

    .. attribute:: id
       :type: int

       The unique ID of this reward type. In the API payload, this
       field is called ``reward_type_id``.

    .. attribute:: description
       :type: str

       A description of what this reward type is used for.

    .. attribute:: count_min
       :type: str | None

       The minimum number of rewarded items/currency.

    .. attribute:: count_max
       :type: str | None

       The maximum number of rewarded items/currency.

    .. attribute:: param*
       :type: str | None

       Descriptions of what the corresponding parameter is used for in
       rewards of this type.
    """

    collection = 'reward_type'
    data: RewardTypeData
    id_field = 'reward_type_id'
    _model = RewardTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str
    count_min: str | None
    count_max: str | None
    param1: str
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None


class Reward(Cached, cache_size=50, cache_ttu=60.0):
    """A reward awarded to a player.

    Access the corresponding :class:`auraxium.ps2.RewardType` instance
    via the :meth:`Reward.type` method for information on generic
    parameters.

    .. attribute:: id
       :type: int

       The unique ID of this reward. In the API payload, this field is
       called ``reward_id``.

    .. attribute:: reward_type_id
       :type: int

       The :class:`~auraxium.ps2.RewardType` of this reward.

       .. seealso::

          :meth:`type` -- The reward type instance for this report.

    .. attribute:: count_min
       :type: int

       The minimum number of rewarded items/currency.

    .. attribute:: count_max
       :type: int

       The maximum number of rewarded items/currency.

    .. attribute:: param*
       :type: str | None

       Type-specific parameters for this reward. Refer to the
       corresponding :class:`~auraxium.ps2.RewardType` for details.
    """

    collection = 'reward'
    data: RewardData
    id_field = 'reward_id'
    _model = RewardData

    # Type hints for data class fallback attributes
    id: int
    reward_type_id: int
    count_min: int
    count_max: int
    param1: str
    param2: str | None
    param3: str | None
    param4: str | None
    param5: str | None

    @classmethod
    def get_by_reward_group(cls, reward_group_id: int, client: RequestClient
                            ) -> SequenceProxy['Reward']:
        """Return any rewards contained in the given reward group.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'reward_group_to_reward'
        query = Query(collection, service_id=client.service_id)
        query.add_term(field='reward_group_id', value=reward_group_id)
        query.limit(100)
        join = query.create_join(Reward.collection)
        join.set_fields(Reward.id_field)
        return SequenceProxy(Reward, query, client=client)

    @classmethod
    def get_by_reward_set(cls, reward_set_id: int, client: RequestClient
                          ) -> SequenceProxy['Reward']:
        """Return any rewards contained in the given reward set.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'reward_set_to_reward_group'
        query = Query(collection, service_id=client.service_id)
        query.add_term(field='reward_set_id', value=reward_set_id)
        query.limit(100)
        join = query.create_join('reward_group_to_reward').set_list(True)
        join.set_fields('reward_group_id')
        nested = join.create_join(Reward.collection)
        nested.set_fields(Reward.id_field)
        return SequenceProxy(Reward, query, client=client)

    def type(self) -> InstanceProxy[RewardType]:
        """Return the type of reward.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(
            RewardType.collection, service_id=self._client.service_id)
        query.add_term(
            field=RewardType.id_field, value=self.data.reward_type_id)
        return InstanceProxy(RewardType, query, client=self._client)
