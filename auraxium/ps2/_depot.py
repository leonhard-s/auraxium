"""Bundles and special offer class definitions."""

from typing import Final, List, Optional, Tuple

from ..base import Named, Cached
from ..census import Query
from ..models import MarketingBundleData, MarketingBundleSingleData
from .._proxy import InstanceProxy
from .._rest import extract_payload
from ..types import LocaleData

from ._item import Item

__all__ = [
    'MarketingBundle',
    'MarketingBundleSingle'
]


class MarketingBundle(Named, cache_size=100, cache_ttu=60.0):
    """A marketing bundle containing multiple items.

    A purchaseable bundle in the in-game depot. Use the :meth:`items`
    method to retrieve the items contained in this bundle.

    .. attribute:: id
       :type: int

       The unique ID of this bundle. In the API payload, this
       field is called ``marketing_bundle_id``.

    .. attribute:: description
       :type: auraxium.types.LocaleData

       The description text for this bundle.

    .. attribute:: image_id
       :type: int

       The image asset ID for this bundle.

    .. attribute:: cert_price
       :type: int | None

       The unlock price in certification points, if any. Note that most
       promotional bundles may only be unlocked via Daybreak Cash.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised display name of the bundle.

    .. attribute:: station_cash_price
       :type: int

       The unlock price in Daybreak Cash (formerly SOE Station Cash).

    .. attribute:: release_time
       :type: int

       The time at which this bundle was first released as a UTC
       timestamp.
    """

    collection = 'marketing_bundle'
    data: MarketingBundleData
    id_field = 'marketing_bundle_id'
    _model = MarketingBundleData

    # Type hints for data class fallback attributes
    id: int
    description: LocaleData
    image_id: int
    cert_price: Optional[int]
    name: LocaleData
    station_cash_price: int
    release_time: int

    def image(self) -> str:
        """Return the default image for this type."""
        image_id: int = self.data.image_id  # type: ignore
        url = 'https://census.daybreakgames.com/files/ps2/images/static/'
        return url + f'{image_id}.png'

    async def items(self) -> List[Tuple[Item, int]]:
        """Return the contents of the bundle.

        This returns a list of tuples consisting of the item and the
        quantity awarded.
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
            count = int(str(item_data['quantity']))
            items.append((item, count))
        return items


class MarketingBundleSingle(Cached, cache_size=100, cache_ttu=60.0):
    """A marketing bundle containing a single item.

    This is used for single-item entries in the depot, such as weapons,
    scopes or other upgrades that can be purchased in the Depot.

    .. attribute:: id
       :type: int

       The unique ID of this bundle. In the API payload, this
       field is called ``marketing_bundle_id``.

    .. attribute:: item_id
       :type: int

       The :class:`auraxium.ps2.Item` unlocked by this bundle.

    .. attribute:: item_quantity
       :type: int

       The number of items received.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised display name of the bundle.

    .. attribute:: station_cash_price
       :type: int

       The unlock price in Daybreak Cash (formerly SOE Station Cash).

    .. attribute:: cert_price
       :type: int | None

       The certification point price of the item, if any.

    .. attribute:: release_time
       :type: int

       The time at which this item was first released as a UTC
       timestamp.
    """

    collection = 'marketing_bundle_with_1_item'
    data: MarketingBundleSingleData
    id_field = 'marketing_bundle_id'
    _model = MarketingBundleSingleData

    # Type hints for data class fallback attributes
    id: int
    item_id: int
    item_quantity: int
    name: LocaleData
    station_cash_price: int
    cert_price: Optional[int]
    release_time: int

    def item(self) -> InstanceProxy[Item]:
        """Return the item unlocked by the bundle.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=self.data.item_id)
        return InstanceProxy(Item, query, client=self._client)
