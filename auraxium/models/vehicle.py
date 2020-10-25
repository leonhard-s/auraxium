"""Data classes for :mod:`auraxium.ps2.vehicle`."""

from typing import Optional

from ..base import ImageData, Ps2Data
from ..types import LocaleData

__all__ = [
    'VehicleAttachmentData',
    'VehicleData'
]


class VehicleAttachmentData(Ps2Data):
    """Data class for :class:`auraxium.ps2.vehicle.VehicleAttachment`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        item_id: The item that is being attached.
        vehicle_id: The vehicle the item may be attached to.
        faction_id: The faction for which this attachment is available.
        description: A description of the attachment.
        slot_id: The slot the attachment goes into.

    """

    item_id: int
    vehicle_id: int
    faction_id: int
    description: str
    slot_id: int


class VehicleData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.vehicle.Vehicle`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        vehicle_id: The unique ID of this vehicle.
        name: The localised name of the vehicle.
        description: The localised description of the vehicle.
        type_id: The type of vehicle.
        type_name: The name of the type of vehicle.
        cost: The cost of the vehicle.
        cost_resource_id: The ID of the resource the cost is in.

    """

    vehicle_id: int
    name: LocaleData
    description: LocaleData
    type_id: int
    type_name: str
    cost: Optional[int] = None
    cost_resource_id: Optional[int] = None
