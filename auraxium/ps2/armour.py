"""Armor mapping class definitions."""

import enum

from ..base import Cached
from ..models import ArmourInfoData
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
