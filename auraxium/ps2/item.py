import dataclasses
import logging
from typing import ClassVar, Optional, TYPE_CHECKING

from ..base import Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
from ..image import CensusImage
from ..proxy import InstanceProxy
from ..types import CensusData
from ..utils import LocaleData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. During runtime, this would cause a circular import.
    from .weapon import Weapon

log = logging.getLogger('auraxium.ps2')


@dataclasses.dataclass(frozen=True)
class ItemData(Ps2Data):
    item_id: int
    item_type_id: int
    item_category_id: int
    activatable_ability_id: Optional[int]
    passive_ability_id: Optional[int]
    is_vehicle_weapon: bool
    name: LocaleData
    description: LocaleData
    faction_id: int
    max_stack_size: int
    image_set_id: int
    # image_id: int
    skill_set_id: Optional[int]
    is_default_attachment: bool

    @classmethod
    def from_census(cls, data: CensusData) -> 'ItemData':
        active_ability = data.get('activatable_ability_id', None)
        if active_ability is not None:
            active_ability = int(active_ability)
        passive_ability = data.get('passive_ability_id', None)
        if passive_ability is not None:
            passive_ability = int(passive_ability)
        skill_set = data.get('skill_set_id')
        if skill_set is not None:
            skill_set = int(skill_set)
        if (image_set_id := data.get('image_set_id')) is not None:
            image_set_id = int(image_set_id)
        return cls(
            # Required
            int(data['item_id']),
            int(data['item_type_id']),
            int(data['item_category_id']),
            # Optional
            active_ability,
            passive_ability,
            bool(data['is_vehicle_weapon']),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['faction_id']),
            int(data['max_stack_size']),
            image_set_id,
            skill_set,
            bool(data['is_default_attachment']))


class Item(Named, cache_size=128, cache_ttu=3600.0):

    _cache: ClassVar[TLRUCache[int, 'Item']]  # type: ignore
    _collection = 'item'
    data: ItemData
    _id_field = 'item_id'

    def _build_dataclass(self, data: CensusData) -> ItemData:
        return ItemData.from_census(data)

    @property
    def image(self) -> CensusImage:
        return CensusImage(self.data.image_set_id, client=self._client)

    def weapon(self) -> InstanceProxy['Weapon']:
        from .weapon import Weapon
        query = Query('item_to_weapon', service_id=self._client.service_id)
        query.add_term(field=self._id_field, value=self.id)
        join = query.create_join('weapon')
        join.parent_field = 'weapon_id'
        proxy: InstanceProxy['Weapon'] = InstanceProxy(
            Weapon, query, client=self._client)
        return proxy
