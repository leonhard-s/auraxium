"""Data classes for :mod:`auraxium.ps2.currency`."""


import dataclasses

from ..base import Ps2Data
from ..types import CensusData, LocaleData

__all__ = [
    'CurrencyData'
]


@dataclasses.dataclass(frozen=True)
class CurrencyData(Ps2Data):
    """Data class for :class:`auraxium.ps2.currency.Currency`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        currency_id: The unique ID of this currency entry.
        name: The localised name of this currency.
        icon_id: The image ID of the currency icon image asset.
        inventory_cap: The maximum amount of this currency a character
            may hold.

    """

    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'CurrencyData':
        return cls(
            int(data.pop('currency_id')),
            LocaleData.from_census(data.pop('name')),
            int(data.pop('icon_id')),
            int(data.pop('inventory_cap')))
