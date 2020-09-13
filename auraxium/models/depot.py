"""Data classes for :mod:`auraxium.ps2.depot`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional


__all__ = [
    'MarketingBundleData',
    'MarketingBundleSingleData'
]


@dataclasses.dataclass(frozen=True)
class MarketingBundleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.depot.MarketingBundle`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        marketing_bundle_id: The unique ID of this bundle.
        name: The localised name of the bundle.
        description: The description text for this bundle.
        image_id: The image asset ID for this bundle.
        cert_price: The unlock price in certification points, if any.
        station_cash_price: The unlock price in daybreak cash, if any.
        release_time: The time at which this bundle was first released
            as a UTC timestamp.

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
            int(data.pop('marketing_bundle_id')),
            LocaleData.from_census(data.pop('name')),
            LocaleData.from_census(data.pop('description')),
            int(data.pop('image_id')),
            optional(data, 'cert_price', int),
            int(data.pop('station_cash_price')),
            int(data.pop('release_time')))


@dataclasses.dataclass(frozen=True)
class MarketingBundleSingleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.depot.MarketingBundleSingle`.

    This is generally used for the single-item "bundles" in the depot,
    i.e. any single weapon or cosmetic purchasable on its own.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        marketing_bundle_id: The unique ID of this bundle.
        item_id: The item unlocked by this bundle.
        item_quantity: The number of items received.
        station_cash_price: The daybreak cash price of the item.
        cert_price: The certification point price of the item.
        release_time: The time at which this item was first released
            as a UTC timestamp.

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
            int(data.pop('marketing_bundle_id')),
            int(data.pop('item_id')),
            int(data.pop('item_quantity')),
            int(data.pop('station_cash_price')),
            optional(data, 'cert_price', int),
            int(data.pop('release_time')))
