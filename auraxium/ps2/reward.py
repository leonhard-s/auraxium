"""Reward and reward type class definitions."""

from typing import Final, Optional

from ..base import Cached
from ..census import Query
from ..client import Client
from ..models import RewardData, RewardTypeData
from ..proxy import InstanceProxy, SequenceProxy


class RewardType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of reward.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'reward_type'
    data: RewardTypeData
    dataclass = RewardTypeData
    id_field = 'reward_type_id'

    # Type hints for data class fallback attributes
    reward_type_id: int
    description: str
    count_min: Optional[str]
    count_max: Optional[str]
    param1: str
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]


class Reward(Cached, cache_size=50, cache_ttu=60.0):
    """A reward awarded to a player.

    Access the corresponding :class:`auraxium.ps2.reward.RewardType`
    instance via the :meth:`type` method for information on generic
    parameters.
    """

    collection = 'reward'
    data: RewardData
    dataclass = RewardData
    id_field = 'reward_id'

    # Type hints for data class fallback attributes
    reward_id: int
    reward_type_id: int
    count_min: int
    count_max: int
    param1: str
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]

    @classmethod
    def get_by_reward_group(cls, reward_group_id: int, client: Client
                            ) -> SequenceProxy['Reward']:
        """Return any rewards contained in the given reward group."""
        collection: Final[str] = 'reward_group_to_reward'
        query = Query(collection, service_id=client.service_id)
        query.add_term(field='reward_group_id', value=reward_group_id)
        query.limit(100)
        join = query.create_join(Reward.collection)
        join.set_fields(Reward.id_field)
        return SequenceProxy(Reward, query, client=client)

    @classmethod
    def get_by_reward_set(cls, reward_set_id: int, client: Client
                          ) -> SequenceProxy['Reward']:
        """Return any rewards contained in the given reward set."""
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
        """Return the type of reward."""
        query = Query(
            RewardType.collection, service_id=self._client.service_id)
        query.add_term(
            field=RewardType.id_field, value=self.data.reward_type_id)
        return InstanceProxy(RewardType, query, client=self._client)
