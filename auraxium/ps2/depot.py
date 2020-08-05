"""Bundles and special offer class definitions."""

import dataclasses
from typing import Final, List, Optional, Tuple

from ..base import Named, Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy
from ..request import extract_payload
from ..types import CensusData
from ..utils import LocaleData, optional

from .item import Item


@dataclasses.dataclass(frozen=True)
class MarketingBundleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.depot.MarketingBundle`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    marketing_bundle_id: int
    name: LocaleData
    description: LocaleData
    image_id: int
    cert_price: Optional[int]
    station_cash_price: int
    release_time: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'MarketingBundleData':
        return cls(
            int(data['marketing_bundle_id']),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['image_id']),
            optional(data, 'cert_price', int),
            int(data['station_cash_price']),
            int(data['release_time']))


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
        join.parent_field = join.child_field = Item.id_field
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        key_name = f'{Item.id_field}_join_{Item.collection}'
        items: List[Tuple[Item, int]] = []
        for item_data in data:
            item = Item(item_data[key_name], client=self._client)
            count = int(item_data['quantity'])
            items.append((item, count))
        return items


@dataclasses.dataclass(frozen=True)
class MarketingBundleSingleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.depot.MarketingBundleSingle`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    marketing_bundle_id: int
    item_id: int
    item_quantity: int
    station_cash_price: int
    cert_price: Optional[int]
    release_time: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'MarketingBundleSingleData':
        return cls(
            int(data['marketing_bundle_id']),
            int(data['item_id']),
            int(data['item_quantity']),
            int(data['station_cash_price']),
            optional(data, 'cert_price', int),
            int(data['release_time']))


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
