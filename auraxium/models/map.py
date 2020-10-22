"""Data classes for :mod:`auraxium.ps2.map`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData, LocaleData, optional

__all__ = [
    'FacilityTypeData',
    'MapHexData',
    'MapRegionData',
    'RegionData'
]


@dataclasses.dataclass(frozen=True)
class FacilityTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.FacilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        facility_type_id: The unique ID of this facility type.
        description: The description of this facility type.

    """

    facility_type_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'FacilityTypeData':
        return cls(
            int(data.pop('facility_type_id')),
            str(data.pop('description')))


@dataclasses.dataclass(frozen=True)
class MapHexData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        zone_id: The ID of the zone (or continent) containing this hex.
        map_region_id: The ID of the map region associated with this
            hex.
        x: The X map position of the hex.
        y: The Y map position of the hex.
        hex_type: The type of map hex. Refer to :attr:`type_name` for
            details.
        type_name: The name of the hex' type.

    """

    # pylint: disable=invalid-name

    zone_id: int
    map_region_id: int
    x: int
    y: int
    hex_type: int
    type_name: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'MapHexData':
        return cls(
            int(data.pop('zone_id')),
            int(data.pop('map_region_id')),
            int(data.pop('x')),
            int(data.pop('y')),
            int(data.pop('hex_type')),
            str(data.pop('type_name')))


@dataclasses.dataclass(frozen=True)
class MapRegionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        map_region_id: The unique ID of this map region.
        zone_id: The ID of the zone (i.e. continent) this region is in.
        facility_id: The ID of the associated facility.
        facility_name: The name of the associated facility.
        facility_type_id: The type ID of the associated facility.
        facility_type: The type name of the associated facility.
        location_x: The X world position of the facility.
        location_y: The Y world position of the facility.
        location_z: The Z world position of the facility.
        reward_amount: (Unused)
        reward_currency_id: (Unused)

    """

    map_region_id: int
    zone_id: int
    facility_id: int
    facility_name: str
    facility_type_id: int
    facility_type: str
    location_x: Optional[float]
    location_y: Optional[float]
    location_z: Optional[float]
    reward_amount: Optional[int]
    reward_currency_id: Optional[int]

    @classmethod
    def from_census(cls, data: CensusData) -> 'MapRegionData':
        return cls(
            int(data.pop('map_region_id')),
            int(data.pop('zone_id')),
            int(data.pop('facility_id')),
            str(data.pop('facility_name')),
            int(data.pop('facility_type_id')),
            str(data.pop('facility_type')),
            optional(data, 'location_x', float),
            optional(data, 'location_y', float),
            optional(data, 'location_z', float),
            optional(data, 'reward_amount', int),
            optional(data, 'reward_currency_id', int))


@dataclasses.dataclass(frozen=True)
class RegionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.Region`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        region_id: The unique ID of the map region.
        zone_id: The ID of the zone (i.e. continent) the region is in.
        initial_faction_id: (Unused)
        name: The localised name of the map region.

    """

    region_id: int
    zone_id: int
    initial_faction_id: int
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'RegionData':
        return cls(
            int(data.pop('region_id')),
            int(data.pop('zone_id')),
            int(data.pop('initial_faction_id')),
            LocaleData.from_census(data.pop('name')))
