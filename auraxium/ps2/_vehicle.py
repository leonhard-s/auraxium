"""Vehicle class definitions."""

from typing import Final, List, Optional, Union

from ..base import Cached, ImageMixin, Named
from ..census import Query
from ..models import VehicleAttachmentData, VehicleData
from .._rest import RequestClient
from .._proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from ._faction import Faction
from ._item import Item
from ._skill import SkillSet

__all__ = [
    'Vehicle',
    'VehicleAttachment'
]


class Vehicle(Named, ImageMixin, cache_size=50, cache_ttu=3600.0):
    """A mountable vehicle in PlanetSide 2.

    This includes aircraft and ground vehicles, as well as mountable
    turrets and constructible.

    .. attribute:: id
       :type: int

       The unique ID of this vehicle type. In the API payload, this field
       is called ``vehicle_id``.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description of the vehicle type.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the vehicle.

    .. attribute:: type_id
       :type: int

       The type of vehicle.

    .. attribute:: type_name
       :type: str

       The name of the type of vehicle.

    .. attribute:: cost
       :type: int | None

       The spawn cost of the vehicle.

    .. attribute:: cost_resource_id
       :type: int | None

       The ID of the resource the vehicle costs.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'vehicle'
    data: VehicleData
    id_field = 'vehicle_id'
    _model = VehicleData

    # Type hints for data class fallback attributes
    id: int
    description: Optional[LocaleData]
    name: LocaleData
    type_id: int
    type_name: str
    cost: Optional[int]
    cost_resource_id: Optional[int]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def factions(self) -> SequenceProxy[Faction]:
        """Return the factions that have access to this vehicle.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'vehicle_faction'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.id)
        query.limit(5)
        return SequenceProxy(Faction, query, client=self._client)

    @classmethod
    async def get_by_faction(cls, faction: Union[Faction, int], *,
                             client: RequestClient) -> List['Vehicle']:
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

        This returns a :class:`auraxium.SequenceProxy`.
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


class VehicleAttachment(Cached, cache_size=250, cache_ttu=180.0):
    """Links vehicles to the items and attachments they support.

    .. attribute:: id
       :type: int

       The item that is being attached. In the API payload, this field
       is called ``vehicle_attachment_id``.

    .. attribute:: vehicle_id
       :type: int

       The ID of the :class:`Vehicle` the item may be attached to.

       .. seealso::

          :meth:`vehicle` -- The vehicle the item may be attached to.

    .. attribute:: faction_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Faction` for which this
       attachment is available.

       .. seealso::

          :meth:`faction` -- The faction the attachment is availabl
          to.

    .. attribute:: description
       :type: str

       A description of the attachment.

    .. attribute:: slot_id
       :type: int

       The slot the attachment goes into.
    """

    collection = 'vehicle_attachment'
    data: VehicleAttachmentData
    id_field = 'vehicle_attachment_id'
    _model = VehicleAttachmentData

    # Type hints for data class fallback attributes
    id: int
    vehicle_id: int
    faction_id: int
    description: str
    slot_id: int

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction this attachment is available to.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def item(self) -> InstanceProxy[Item]:
        """Return the attachable item for the vehicle.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=self.data.item_id)
        return InstanceProxy(Item, query, client=self._client)

    def vehicle(self) -> InstanceProxy[Vehicle]:
        """Return the vehicle the item may be attached to.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Vehicle.collection, service_id=self._client.service_id)
        query.add_term(field=Vehicle.id_field, value=self.data.vehicle_id)
        return InstanceProxy(Vehicle, query, client=self._client)
