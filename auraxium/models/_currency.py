"""Data classes for :mod:`auraxium.ps2._currency`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'CurrencyData'
]


class CurrencyData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Currency`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int
