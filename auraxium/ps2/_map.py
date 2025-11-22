"""Facility and map class definitions."""

from typing import Final, Set

from ..base import Cached, Named
from ..census import Query
from ..models import FacilityTypeData, MapHexData, MapRegionData, RegionData
from .._proxy import InstanceProxy, SequenceProxy
from .._rest import RequestClient
from ..types import LocaleData

from ._zone import Zone

__all__ = [
    'FacilityType',
    'MapHex',
    'MapRegion',
    'Region'
]


class FacilityType(Cached, cache_size=10, cache_ttu=3600.0):
    """A type of base/facility found in the game.

    .. attribute:: id
       :type: int

       The unique ID of this facility type. In the API payload, this
       field is called ``facilty_type_id``.

    .. attribute:: description
       :type: str

       An internal description of this facility type.
    """

    collection = 'facility_type'
    data: FacilityTypeData
    id_field = 'facility_type_id'
    _model = FacilityTypeData

    # Type hints for data class fallback attributes
    id: int
    description: str


class MapHex(Cached, cache_size=100, cache_ttu=60.0):
    """An individual territory hex in the map.

    Note that the :attr:`x` and :attr:`y` coordintes are not using a
    regular Cartesian coordinate system. Rather, they are using a
    hexagonal coordinate system, with all hexes being positioned via
    integer coordinates.

    An introduction on hexagonal coordinate systems can be found in
    this article:
    https://www.redblobgames.com/grids/hexagons/#coordinates-axial

    .. note::

       The coordinate system in PlanetSide 2 has its second axis go
       from bottom left to top right, unlike the article above. All of
       the principles and transformations still apply.

    Refer to the following link for a usage example of this type,
    including converting from the hexgonal coordinate system to the
    Cartesian coordinates used on the map screen.

    The module's purpose is to generate serialised SVGs containing
    merged base outlines for a given continent:
    https://github.com/auto-pl/apl-api/blob/main/tools/map_hex_generator.py

    .. attribute:: zone_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Zone` containing this hex.

    .. attribute:: map_region_id
       :type: int

       The ID of the :class:`~auraxium.ps2.MapRegion` associated with
       this hex.

    .. attribute:: x
       :type: int

       The X map position of the hex.

    .. attribute:: y
       :type: int

       The Y map position of the hex.

    .. attribute:: hex_type
       :type: int

       The type of map hex. Refer to :attr:`type_name` for details.

    .. attribute:: type_name
       :type: str

       The name of the hex's type.
    """

    collection = 'map_hex'
    data: MapHexData
    id_field = 'map_region_id'
    _model = MapHexData

    # Type hints for data class fallback attributes
    zone_id: int
    map_region_id: int
    x: int
    y: int
    hex_type: int
    type_name: str

    def map_region(self) -> InstanceProxy['MapRegion']:
        """Return the map region associated with this map hex."""
        query = Query(MapRegion.collection, service_id=self._client.service_id)
        query.add_term(field=MapRegion.id_field, value=self.data.map_region_id)
        return InstanceProxy(MapRegion, query, client=self._client)


class MapRegion(Cached, cache_size=100, cache_ttu=60.0):
    """A facility on the continent map.

    .. attribute:: id
       :type: int

       The unique ID of this map region. In the API payload, this
       field is called ``map_region_id``.

    .. attribute:: zone_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Zone` containing this hex.

    .. attribute:: facility_id
       :type: int | None

       The ID of the associated facility.

       .. note::

          Facilities are not available as an API datatype, but are
          referenced by facility capture events.

          Use the :meth:`get_by_facility_id` method to look up a map
          region by its associated facility ID.

    .. attribute:: facility_name
       :type: str

       The display name of the associated facility.

    .. attribute:: facility_type_id
       :type: int | None

       The ID of the :class:`FacilityType` of the map region.

    .. attribute:: facility_type
       :type: str | None

       The type name of the associated facility.

    .. attribute:: location_x
       :type: float | None

       The X world position of the facility.

       The coordinate system used goes from -4096 to +4096 for normal
       continents, with the origin in the centre of the continent.

       The map X axis points North (i.e. up on the map screen).

    .. attribute:: location_y
       :type: float | None

       The Y world position of the facility.

       The map Y axis points upwards from the map plane and represents
       the elevation of the base marker in the first person UI.

    .. attribute:: location_z
       :type: float | None

       The Z world position of the facility.

       The coordinate system used goes from -4096 to +4096 for normal
       continents, with the origin in the centre of the continent.

       The map Z axis points East (i.e. right on the map screen).

    .. attribute:: reward_amount
       :type: int | None

       Unused.

    .. attribute:: reward_currency_id
       :type: int | None

       Unused.
    """

    collection = 'map_region'
    data: MapRegionData
    id_field = 'map_region_id'
    _model = MapRegionData

    # Type hints for data class fallback attributes
    id: int
    zone_id: int
    facility_id: int | None
    facility_name: str
    facility_type_id: int | None
    facility_type: str | None
    location_x: float | None
    location_y: float | None
    location_z: float | None
    reward_amount: int | None
    reward_currency_id: int | None

    @classmethod
    def get_by_facility_id(cls, facility_id: int, client: RequestClient
                           ) -> InstanceProxy['MapRegion']:
        """Return a map region by its facility ID.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(cls.collection, service_id=client.service_id,
                      facility_id=facility_id)
        return InstanceProxy(MapRegion, query, client=client)

    async def get_connected(self) -> Set['MapRegion']:
        """Return the facilities connected to this region."""
        if self.data.facility_id is None:
            return set()
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
        proxy: SequenceProxy[MapRegion] = SequenceProxy(
            MapRegion, query, client=self._client)
        connected.update(await proxy.flatten())
        # Modified query B
        query.data.terms = []
        query.add_term(field='facility_id_b', value=self.data.facility_id)
        proxy = SequenceProxy(MapRegion, query, client=self._client)
        connected.update(await proxy.flatten())
        return connected

    def zone(self) -> InstanceProxy[Zone]:
        """Return the zone/continent of the region.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Zone.collection, service_id=self._client.service_id)
        query.add_term(field=Zone.id_field, value=self.data.zone_id)
        return InstanceProxy(Zone, query, client=self._client)


class Region(Named, cache_size=100, cache_ttu=60.0):
    """A map region or facility.

    .. attribute:: region_id
       :type: int

       The unique ID of the map region. In the API payload, this
       field is called ``region_id``.

    .. attribute:: zone_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Zone` containing this hex.

    .. attribute:: initial_faction_id
       :type: int

       Unused.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of the map region.
    """

    collection = 'region'
    data: RegionData
    id_field = 'region_id'
    _model = RegionData

    # Type hints for data class fallback attributes
    id: int
    zone_id: int
    initial_faction_id: int
    name: LocaleData

    def map_region(self) -> InstanceProxy[MapRegion]:
        """Return the map region associated with this region.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(MapRegion.collection, service_id=self._client.service_id)
        query.add_term(field=MapRegion.id_field, value=self.id)
        return InstanceProxy(MapRegion, query, client=self._client)

    def zone(self) -> InstanceProxy[Zone]:
        """Return the zone/continent of the region.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Zone.collection, service_id=self._client.service_id)
        query.add_term(field=Zone.id_field, value=self.data.zone_id)
        return InstanceProxy(Zone, query, client=self._client)
