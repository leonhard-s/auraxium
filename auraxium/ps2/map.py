"""Facility and map class definitions."""

import dataclasses
from typing import Optional

from ..base import Cached, Named, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .zone import Zone


@dataclasses.dataclass(frozen=True)
class FacilityTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.FacilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    facility_type_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'FacilityTypeData':
        return cls(
            int(data['facility_type_id']),
            str(data['description']))


class FacilityType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of base/facility found in the game."""

    collection = 'facility_type'
    data: FacilityTypeData
    id_field = 'facility_type_id'

    def _build_dataclass(self, data: CensusData) -> FacilityTypeData:
        return FacilityTypeData.from_census(data)


@dataclasses.dataclass(frozen=True)
class MapHexData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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
            int(data['zone_id']),
            int(data['map_region_id']),
            int(data['x']),
            int(data['y']),
            int(data['hex_type']),
            str(data['type_name']))


class MapHex(Cached, cache_size=100, cache_ttu=60.0):
    """An individual territory hex in the map."""

    collection = 'map_hex'
    data: MapHexData
    id_field = 'map_hex_id'

    def _build_dataclass(self, data: CensusData) -> MapHexData:
        return MapHexData.from_census(data)


@dataclasses.dataclass(frozen=True)
class MapRegionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    map_region_id: int
    zone_id: int
    facility_id: int
    facility_name: str
    facility_type_id: int
    facility_type: str
    location_x: float
    location_y: float
    location_z: float
    reward_amount: Optional[int]
    reward_currency_id: Optional[int]

    @classmethod
    def from_census(cls, data: CensusData) -> 'MapRegionData':
        return cls(
            int(data['map_region_id']),
            int(data['zone_id']),
            int(data['facility_id']),
            str(data['facility_name']),
            int(data['facility_type_id']),
            str(data['facility_type']),
            float(data['location_x']),
            float(data['location_y']),
            float(data['location_z']),
            optional(data, 'reward_amount', int),
            optional(data, 'reward_currency_di', int))


class MapRegion(Cached, cache_size=100, cache_ttu=60.0):
    """A facility on the continent map."""

    collection = 'map_region'
    data: MapRegionData
    id_field = 'map_region_id'

    def _build_dataclass(self, data: CensusData) -> MapRegionData:
        return MapRegionData.from_census(data)

    # def reward_currency(self) -> InstanceProxy[Reward]

    def zone(self) -> InstanceProxy[Zone]:
        """Return the zone/continent of the region.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Zone.collection, service_id=self._client.service_id)
        query.add_term(field=Zone.id_field, value=self.data.zone_id)
        return InstanceProxy(Zone, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class RegionData(Ps2Data):
    """Data class for :class:`auraxium.ps2.map.Region`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    region_id: int
    zone_id: int
    initial_faction_id: int  #: No longer used
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'RegionData':
        return cls(
            int(data['region_id']),
            int(data['zone_id']),
            int(data['initial_faction_id']),
            LocaleData.from_census(data['name']))


class Region(Named, cache_size=100, cache_ttu=60.0):
    """A map region or facility."""

    collection = 'region'
    data: RegionData
    id_field = 'region_id'

    def _build_dataclass(self, data: CensusData) -> RegionData:
        return RegionData.from_census(data)

    def map_region(self) -> InstanceProxy[MapRegion]:
        """Return the map region associated with this region.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(MapRegion.collection, service_id=self._client.service_id)
        query.add_term(field=MapRegion.id_field, value=self.id)
        return InstanceProxy(MapRegion, query, client=self._client)

    def zone(self) -> InstanceProxy[Zone]:
        """Return the zone/continent of the region.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Zone.collection, service_id=self._client.service_id)
        query.add_term(field=Zone.id_field, value=self.data.zone_id)
        return InstanceProxy(Zone, query, client=self._client)
