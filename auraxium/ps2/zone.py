"""Zone class definition."""

import dataclasses

from ..base import Named, Ps2Data
from ..types import CensusData
from ..utils import LocaleData


@dataclasses.dataclass(frozen=True)
class ZoneData(Ps2Data):
    """Data class for :class:`auraxium.ps2.zone.Zone`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_id: int
    code: str
    hex_size: int
    name: LocaleData
    description: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'ZoneData':
        return cls(
            int(data['zone_id']),
            str(data['code']),
            int(data['hex_size']),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']))


class Zone(Named, cache_size=20, cache_ttu=3600.0):
    """A continent or dynamic zone in the game world.

    Note that some dynamic zones are not resolvable via this object.
    Dynamic zones include Sanctuary, the Tutorial zones, and the outfit
    wars desolation maps.
    """

    collection = 'zone'
    data: ZoneData
    id_field = 'zone_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ZoneData:
        return ZoneData.from_census(data)
