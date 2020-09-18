"""Facility and map class definitions."""

import dataclasses
from typing import Final, Optional, Set

from ..base import Cached, Named, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .zone import Zone


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
            int(data['facility_type_id']),
            str(data['description']))


class FacilityType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of base/facility found in the game."""

    collection = 'facility_type'
    data: FacilityTypeData
    id_field = 'facility_type_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> FacilityTypeData:
        return FacilityTypeData.from_census(data)


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

    @staticmethod
    def _build_dataclass(data: CensusData) -> MapHexData:
        return MapHexData.from_census(data)

    def map_region(self) -> InstanceProxy['MapRegion']:
        """Return the map region associated with this map hex."""
        query = Query(MapRegion.collection, service_id=self._client.service_id)
        query.add_term(field=MapRegion.id_field, value=self.data.map_region_id)
        return InstanceProxy(MapRegion, query, client=self._client)


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
            int(data['map_region_id']),
            int(data['zone_id']),
            int(data['facility_id']),
            str(data['facility_name']),
            int(data['facility_type_id']),
            str(data['facility_type']),
            optional(data, 'location_x', float),
            optional(data, 'location_y', float),
            optional(data, 'location_z', float),
            optional(data, 'reward_amount', int),
            optional(data, 'reward_currency_di', int))


class MapRegion(Cached, cache_size=100, cache_ttu=60.0):
    """A facility on the continent map."""

    collection = 'map_region'
    data: MapRegionData
    id_field = 'map_region_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> MapRegionData:
        return MapRegionData.from_census(data)

    async def get_connected(self) -> Set['MapRegion']:
        """Return the facilities connected to this region."""
        # NOTE: This operation cannot be done in a single query as there is no
        # "or" operator.
        collection: Final[str] = 'facility_link'
        connected: Set['MapRegion'] = set()
        # Set up the base query
        query = Query(collection, service_id=self._client.service_id)
        query.limit(10)
        join = query.create_join(self.collection)
        join.set_fields('facility_id_a', 'facility_id')
        join = query.create_join(self.collection)
        join.set_fields('facility_id_b', 'facility_id')
        # Modified query A
        query.add_term(field='facility_id_a', value=self.data.facility_id)
        proxy: SequenceProxy[MapRegion]
        proxy = SequenceProxy(MapRegion, query, client=self._client)
        connected.update(await proxy.flatten())
        # Modified query B
        query.data.terms = []
        query.add_term(field='facility_id_b', value=self.data.facility_id)
        proxy = SequenceProxy(MapRegion, query, client=self._client)
        connected.update(await proxy.flatten())
        return connected

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
            int(data['region_id']),
            int(data['zone_id']),
            int(data['initial_faction_id']),
            LocaleData.from_census(data['name']))


class Region(Named, cache_size=100, cache_ttu=60.0):
    """A map region or facility."""

    collection = 'region'
    data: RegionData
    id_field = 'region_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> RegionData:
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
