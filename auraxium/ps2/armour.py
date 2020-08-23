"""Armor mapping class definitions."""

import dataclasses
import enum
from typing import Optional

from ..base import Cached, Ps2Data
from ..utils import optional
from ..types import CensusData


class ArmourFacing(enum.IntEnum):
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
class ArmourInfoData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ArmorInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        armor_info_id: The unique ID of this entry.
        armor_facing_id: The enum value the facing direction this entry
            provides armour data for.
        armor_percent: Damage reduction in percent.
        armor_amount: A flat damage absorption applied to the damage
            effect; generally unused.
        description: A description for this entry.

    """

    armor_info_id: int
    armor_facing_id: int
    armor_percent: int
    armor_amount: Optional[int]
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ArmourInfoData':
        return cls(
            int(data['armor_info_id']),
            int(data['armor_facing_id']),
            int(data['armor_percent']),
            optional(data, 'armor_amount', int),
            str(data['description']))


class ArmourInfo(Cached, cache_size=100, cache_ttu=60.0):
    """An armour stat for a given entity.

    Note that any given entity may have multiple :class:`ArmourInfo`
    instances associated with it, one for each :class:`ArmourFacing`
    value.
    """

    collection = 'armor_info'
    data: ArmourInfoData
    id_field = 'armor_info_id'

    @property
    def facing(self) -> ArmourFacing:
        """Return the facing direction for this stat entry."""
        return ArmourFacing(self.data.armor_info_id)

    @staticmethod
    def _build_dataclass(data: CensusData) -> ArmourInfoData:
        return ArmourInfoData.from_census(data)
