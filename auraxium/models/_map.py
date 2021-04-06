"""Data classes for :mod:`auraxium.ps2.map`."""

from typing import Optional

from ._base import RESTPayload
from ..types import LocaleData

__all__ = [
    'FacilityTypeData',
    'MapHexData',
    'MapRegionData',
    'RegionData'
]

# pylint: disable=too-few-public-methods


class FacilityTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.map.FacilityType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    facility_type_id: int
    description: str


class MapHexData(RESTPayload):
    """Data class for :class:`auraxium.ps2.map.MapHex`.

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
    """Data class for :class:`auraxium.ps2.map.MapHex`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    # NOTE: "SWG" stands for "The Shattered Warpgate" on Esamir
    map_region_id: int
    zone_id: int
    facility_id: Optional[int] = None  # Only missing for SWG
    facility_name: str
    facility_type_id: Optional[int] = None  # Only missing for SWG
    facility_type: Optional[str] = None  # Only missing for SWG
    location_x: Optional[float] = None
    location_y: Optional[float] = None
    location_z: Optional[float] = None
    reward_amount: Optional[int] = None
    reward_currency_id: Optional[int] = None


class RegionData(RESTPayload):
    """Data class for :class:`auraxium.ps2.map.Region`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    region_id: int
    zone_id: int
    initial_faction_id: int
    name: LocaleData
