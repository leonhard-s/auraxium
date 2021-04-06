"""Data classes for :mod:`auraxium.ps2.currency`."""

from ._base import RESTPayload
from ..types import LocaleData

__all__ = [
    'CurrencyData'
]

# pylint: disable=too-few-public-methods


class CurrencyData(RESTPayload):
    """Data class for :class:`auraxium.ps2.currency.Currency`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int
