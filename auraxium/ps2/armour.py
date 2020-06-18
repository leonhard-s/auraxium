"""Armor mapping class definitions."""

import dataclasses
import enum
from typing import Awaitable, List, Optional

from ..base import Cached, Ps2Data
from ..utils import optional
from ..types import CensusData


class ArmorFacing(enum.IntEnum):
    """Enumerator for armour facing directions.

    This is used to list different armour values for a vehicle based on
    the angle of attack.
    """

    FRONT = 0
    RIGHT = 1
    TOP = 2
    REAR = 3
    LEFT = 4
    BOTTOM = 5
    ALL = 5


@dataclasses.dataclass(frozen=True)
class ArmorInfoData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ArmorInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    armor_info_id: int
    armor_facing_id: int
    armor_percent: int
    armor_amount: Optional[int]
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ArmorInfoData':
        return cls(
            int(data['armor_info_id']),
            int(data['armor_facing_id']),
            int(data['armor_percent']),
            optional(data, 'armor_amount', int),
            str(data['description']))


class ArmorInfo(Cached, cache_size=100, cache_ttu=60.0):
    """An armour stat for a given entity.

    Note that any given entity may have multiple :class:`ArmorInfo`
    instances associated with it, one for each :class:`ArmorFacing`
    value.
    """

    _collection = 'armor_info'
    data: ArmorInfoData
    _id_field = 'armor_info_id'

    def _build_dataclass(self, data: CensusData) -> ArmorInfoData:
        return ArmorInfoData.from_census(data)
