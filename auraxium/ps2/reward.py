"""Reward and reward type class definitions."""

import dataclasses
from typing import Final, List, Optional

from ..base import Cached, Ps2Data
from ..census import Query
from ..client import Client
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import optional


@dataclasses.dataclass(frozen=True)
class RewardTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ResourceType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        reward_type_id: The unique ID of this reward type.
        description: A description of what this reward type is used
            for.
        count_min: The minimum number of rewarded items/currency.
        count_max: The maximum number of rewarded items/currency.
        param*: Descriptions of what the corresponding parameter is
            used for in rewards of this type.

    """

    reward_type_id: int
    description: str
    count_min: Optional[str]
    count_max: Optional[str]
    param1: str
    param2: Optional[str]
    param3: Optional[str]
    param4: Optional[str]
    param5: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'RewardTypeData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(1, 5)]
        return cls(
            int(data['reward_type_id']),
            str(data['description']),
            optional(data, 'count_min', str),
            optional(data, 'count_max', str),
            str(data['param1']),
            *params)


class RewardType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of reward.

    This class mostly specifies the purpose of any generic parameters.
    """

    collection = 'reward_type'
    data: RewardTypeData
    id_field = 'reward_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> RewardTypeData:
        return RewardTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class RewardData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Reward`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        reward_id: The unique ID of this reward.
        reward_type_id: The :class:`RewardType` of this reward.
        count_min: The minimum number of rewarded items/currency.
        count_max: The maximum number of rewarded items/currency.
        param*: Type-specific parameters for this reward. Refer to the
            corresponding :class:`RewardType` for details.

    """

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
    def from_census(cls, data: CensusData) -> 'RewardData':
        params: List[Optional[str]] = [
            optional(data, f'param{i+1}', str) for i in range(1, 5)]
        return cls(
            int(data['reward_id']),
            int(data['reward_type_id']),
            int(data['count_min']),
            int(data['count_max']),
            str(data['param1']),
            *params)


class Reward(Cached, cache_size=50, cache_ttu=60.0):
    """A reward awarded to a player.

    Access the corresponding :class:`auraxium.ps2.reward.RewardType`
    instance via the :meth:`type` method for information on generic
    parameters.
    """

    collection = 'reward'
    data: RewardData
    id_field = 'reward_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> RewardData:
        return RewardData.from_census(data)

    @classmethod
    def get_by_reward_group(cls, reward_group_id: int, client: Client
                            ) -> SequenceProxy['Reward']:
        """Return any rewards contained in the given reward group."""
        collection: Final[str] = 'reward_group_to_reward'
        query = Query(collection, service_id=client.service_id)
        query.add_term(field='reward_group_id', value=reward_group_id)
        query.limit(100)
        join = query.create_join(Reward.collection)
        join.parent_field = join.child_field = Reward.id_field
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
        join.parent_field = join.child_field = 'reward_group_id'
        nested = join.create_join(Reward.collection)
        nested.parent_field = nested.child_field = Reward.id_field
        return SequenceProxy(Reward, query, client=client)

    def type(self) -> InstanceProxy[RewardType]:
        """Return the type of reward."""
        query = Query(
            RewardType.collection, service_id=self._client.service_id)
        query.add_term(
            field=RewardType.id_field, value=self.data.reward_type_id)
        return InstanceProxy(RewardType, query, client=self._client)
