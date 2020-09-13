"""Data classes for :mod:`auraxium.ps2.armour`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..utils import optional
from ..types import CensusData

__all__ = [
    'ArmourInfoData'
]


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
