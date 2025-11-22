"""Data classes for :mod:`auraxium.ps2._map`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'FacilityTypeData',
    'MapHexData',
    'MapRegionData',
    'RegionData'
]


class FacilityTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.FacilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    facility_type_id: int
    description: str


class MapHexData(RESTPayload):
    """Data class for :class:`auraxium.ps2.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    zone_id: int
    map_region_id: int
    x: int
    y: int
    hex_type: int
    type_name: str


class MapRegionData(RESTPayload):
    """Data class for :class:`auraxium.ps2.MapRegion`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    # NOTE: "SWG" stands for "The Shattered Warpgate" on Esamir
    map_region_id: int
    zone_id: int
    facility_id: int | None = None  # Only missing for SWG
    facility_name: str
    facility_type_id: int | None = None  # Only missing for SWG
    facility_type: str | None = None  # Only missing for SWG
    location_x: float | None = None
    location_y: float | None = None
    location_z: float | None = None
    reward_amount: int | None = None
    reward_currency_id: int | None = None


class RegionData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Region`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    region_id: int
    zone_id: int
    initial_faction_id: int
    name: LocaleData
