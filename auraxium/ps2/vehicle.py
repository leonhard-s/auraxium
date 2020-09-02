"""Vehicle class definitions."""

import dataclasses
from typing import Final, List, Optional, Union

from ..base import Cached, Named, Ps2Data
from ..census import Query
from ..client import Client
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .faction import Faction
from .item import Item
from .skill import SkillSet


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
            name = LocaleData.from_census(data['name'])
        else:
            name = LocaleData.empty()
        if 'description' in data:
            description = LocaleData.from_census(data['description'])
        else:
            description = LocaleData.empty()
        return cls(
            int(data['vehicle_id']),
            name,
            description,
            int(data['type_id']),
            str(data['type_name']),
            optional(data, 'cost', int),
            optional(data, 'cost_resource_id', int),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))


class Vehicle(Named, cache_size=50, cache_ttu=3600.0):
    """A mountable vehicle in PlanetSide 2.

    This includes aircraft and ground vehicles, as well as mountable
    turrets and constructible.
    """

    collection = 'vehicle'
    data: VehicleData
    id_field = 'vehicle_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> VehicleData:
        return VehicleData.from_census(data)

    def factions(self) -> SequenceProxy[Faction]:
        """Return the factions that have access to this vehicle.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'vehicle_faction'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.id)
        query.limit(5)
        return SequenceProxy(Faction, query, client=self._client)

    @classmethod
    async def get_by_faction(cls, faction: Union[Faction, int], *,
                             client: Client) -> List['Vehicle']:
        """Return all vehicles available to the given faction."""
        collection: Final[str] = 'vehicle_faction'
        faction_id = faction.id if isinstance(faction, Faction) else faction
        query = Query(collection, service_id=client.service_id)
        query.add_term(field=Faction.id_field, value=faction_id)
        query.limit(500)
        join = query.create_join(cls.collection)
        join.set_fields(cls.id_field)
        proxy: SequenceProxy['Vehicle'] = SequenceProxy(
            cls, query, client=client)
        return await proxy.flatten()

    def skill_sets(self, faction: Optional[Union[Faction, int]] = None
                   ) -> SequenceProxy[SkillSet]:
        """Return the skill sets associated with this vehicle.

        By default, this will list all skill sets for all empires. Note
        that this may result in duplicate results as some skill sets
        exist for all empires.
        To avoid duplicates, either generate a set from the returned
        proxy, or specify the faction to resolve skill sets for.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'vehicle_skill_set'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        if faction is not None:
            faction = faction.id if isinstance(faction, Faction) else faction
            query.add_term(field=Faction.id_field, value=faction)
        query.limit(500)
        query.sort('display_index')
        join = query.create_join(SkillSet.collection)
        join.set_fields(SkillSet.id_field)
        return SequenceProxy(SkillSet, query, client=self._client)


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
            int(data['item_id']),
            int(data['vehicle_id']),
            int(data['faction_id']),
            str(data['description']),
            int(data['slot_id']))


class VehicleAttachment(Cached, cache_size=250, cache_ttu=180.0):
    """Links vehicles to the items and attachments they support."""

    collection = 'vehicle_attachment'
    data: VehicleAttachmentData
    id_field = 'vehicle_attachment_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> VehicleAttachmentData:
        return VehicleAttachmentData.from_census(data)

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction this attachment is available to.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def item(self) -> InstanceProxy[Item]:
        """Return the attachable item for the vehicle.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=self.data.item_id)
        return InstanceProxy(Item, query, client=self._client)

    def vehicle(self) -> InstanceProxy[Vehicle]:
        """Return the vehicle the item may be attached to.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Vehicle.collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.data.vehicle_id)
        return InstanceProxy(Vehicle, query, client=self._client)
