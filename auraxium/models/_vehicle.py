"""Data classes for :mod:`auraxium.ps2._vehicle`."""

from typing import Optional

from .base import ImageData, RESTPayload
from ..types import LocaleData

__all__ = [
    'VehicleAttachmentData',
    'VehicleData'
]

# pylint: disable=too-few-public-methods


class VehicleAttachmentData(RESTPayload):
    """Data class for :class:`auraxium.ps2.VehicleAttachment`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    item_id: int
    vehicle_id: int
    faction_id: int
    description: str
    slot_id: int


class VehicleData(RESTPayload, ImageData):
    """Data class for :class:`auraxium.ps2.Vehicle`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    vehicle_id: int
    name: LocaleData
    description: Optional[LocaleData] = None
    type_id: int
    type_name: str
    cost: Optional[int] = None
    cost_resource_id: Optional[int] = None
