"""Data classes for :mod:`auraxium.ps2.resist`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import optional

__all__ = [
    'ResistInfoData',
    'ResistTypeData'
]


@dataclasses.dataclass(frozen=True)
class ResistInfoData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistInfo`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        resist_info: The ID of this resist info entry.
        resist_type_id: The ID of the :class:`ResistType` for this
            entry.
        resist_percent: The damage reduction in percent.
        resist_amount: A flat amount of damage to absorb.
        multiplier_when_headshot: A headshot multiplier override to
            apply.
        description: A description of this resist info entry.

    """

    resist_info_id: int
    resist_type_id: int
    resist_percent: Optional[int]
    resist_amount: Optional[int]
    multiplier_when_headshot: Optional[float]
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ResistInfoData':
        return cls(
            int(data['resist_info_id']),
            int(data['resist_type_id']),
            optional(data, 'resist_percent', int),
            optional(data, 'resist_amount', int),
            optional(data, 'multiplier_when_headshot', float),
            str(data['description']))


@dataclasses.dataclass(frozen=True)
class ResistTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.armour.ResistType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        resist_type_id: The unique ID of this resist type.
        description: A description of what this resist type is used
            for.

    """

    resist_type_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ResistTypeData':
        return cls(
            int(data['resist_type_id']),
            str(data['description']))
