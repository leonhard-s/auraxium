import dataclasses
import logging
from typing import ClassVar, Optional, TYPE_CHECKING

from ..base import Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
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
    # image_set_id: int
    # image_id: int
    skill_set_id: Optional[int]
    is_default_attachment: bool

    @classmethod
    def populate(cls, payload: CensusData) -> 'ItemData':
        active_ability = payload.get('activatable_ability_id', None)
        if active_ability is not None:
            active_ability = int(active_ability)
        passive_ability = payload.get('passive_ability_id', None)
        if passive_ability is not None:
            passive_ability = int(passive_ability)
        skill_set = payload.get('skill_set_id')
        if skill_set is not None:
            skill_set = int(skill_set)
        return cls(
            # Required
            int(payload['item_id']),
            int(payload['item_type_id']),
            int(payload['item_category_id']),
            # Optional
            active_ability,
            passive_ability,
            bool(payload['is_vehicle_weapon']),
            LocaleData.populate(payload['name']),
            LocaleData.populate(payload['description']),
            int(payload['faction_id']),
            int(payload['max_stack_size']),
            skill_set,
            bool(payload['is_default_attachment']))


class Item(Named, cache_size=128, cache_ttu=3600.0):

    _cache: ClassVar[TLRUCache[int, 'Item']]  # type: ignore
    _collection = 'item'
    data: ItemData
    _id_field = 'item_id'

    def _build_dataclass(self, payload: CensusData) -> ItemData:
        return ItemData.populate(payload)

    def weapon(self) -> InstanceProxy['Weapon']:
        from .weapon import Weapon
        query = Query('item_to_weapon', service_id=self._client.service_id)
        query.add_term(field=self._id_field, value=self.id)
        join = query.create_join('weapon')
        join.parent_field = 'weapon_id'
        proxy: InstanceProxy['Weapon'] = InstanceProxy(
            Weapon, query, client=self._client)
        return proxy
