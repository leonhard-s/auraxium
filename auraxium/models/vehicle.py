"""Data classes for :mod:`auraxium.ps2.vehicle`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional

__all__ = [
    'VehicleAttachmentData',
    'VehicleData'
]


@dataclasses.dataclass(frozen=True)
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'VehicleAttachmentData':
        return cls(
            int(data.pop('item_id')),
            int(data.pop('vehicle_id')),
            int(data.pop('faction_id')),
            str(data.pop('description')),
            int(data.pop('slot_id')))


@dataclasses.dataclass(frozen=True)
class VehicleData(Ps2Data):
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
        image_set_id: The image set for this vehicle.
        image_id: The default image asset for this vehicle.
        image_path: The path to the default image asset for this
            vehicle.

    """

    vehicle_id: int
    name: LocaleData
    description: LocaleData
    type_id: int
    type_name: str
    cost: Optional[int]
    cost_resource_id: Optional[int]
    image_set_id: Optional[int]
    image_id: Optional[int]
    image_path: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'VehicleData':
        if 'name' in data:
            name = LocaleData.from_census(data.pop('name'))
        else:
            name = LocaleData.empty()
        if 'description' in data:
            description = LocaleData.from_census(data.pop('description'))
        else:
            description = LocaleData.empty()
        return cls(
            int(data.pop('vehicle_id')),
            name,
            description,
            int(data.pop('type_id')),
            str(data.pop('type_name')),
            optional(data, 'cost', int),
            optional(data, 'cost_resource_id', int),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))
