"""Bundles and special offer class definitions."""

from typing import Final, List, Tuple

from ..base import Named, Cached
from ..census import Query
from ..models import MarketingBundleData, MarketingBundleSingleData
from ..proxy import InstanceProxy
from ..request import extract_payload
from ..types import CensusData

from .item import Item


class MarketingBundle(Named, cache_size=100, cache_ttu=60.0):
    """A marketing bundle containing one or more items.

    This is used for special promotions, or for bundles that contain
    multiple items at once.
    """

    collection = 'marketing_bundle'
    data: MarketingBundleData
    id_field = 'marketing_bundle_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> MarketingBundleData:
        return MarketingBundleData.from_census(data)

    async def items(self) -> List[Tuple[Item, int]]:
        """Return the contents of the bundle.

        This returns a list of tuples consisting of the item, followed
        by the quantity.
        """
        collection: Final[str] = 'marketing_bundle_item'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100)
        join = query.create_join(Item.collection)
        join.set_fields(Item.id_field)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        key_name = f'{Item.id_field}_join_{Item.collection}'
        items: List[Tuple[Item, int]] = []
        for item_data in data:
            item = Item(item_data[key_name], client=self._client)
            count = int(item_data['quantity'])
            items.append((item, count))
        return items


class MarketingBundleSingle(Cached, cache_size=100, cache_ttu=60.0):
    """A marketing bundle containing a single item.

    This is used for single-item entries in the depot, such as weapons,
    scopes or other items that do not require any additional
    information.
    """

    collection = 'marketing_bundle_with_1_item'
    data: MarketingBundleSingleData
    id_field = 'marketing_bundle_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> MarketingBundleSingleData:
        return MarketingBundleSingleData.from_census(data)

    def item(self) -> InstanceProxy[Item]:
        """Return the item unlocked by the bundle.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=self.data.item_id)
        return InstanceProxy(Item, query, client=self._client)
