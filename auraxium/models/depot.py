"""Data classes for :mod:`auraxium.ps2.depot`."""

from typing import Optional

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'MarketingBundleData',
    'MarketingBundleSingleData'
]

# pylint: disable=too-few-public-methods


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


class MarketingBundleSingleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.depot.MarketingBundleSingle`.

    This is generally used for the single-item "bundles" in the depot,
    i.e. any single weapon or cosmetic purchasable on its own.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    marketing_bundle_id: int
    item_id: int
    item_quantity: int
    station_cash_price: int
    cert_price: Optional[int]
    release_time: int
