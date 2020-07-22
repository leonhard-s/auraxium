"""Currency class definition."""

import dataclasses

from ..base import Cached, Ps2Data
from ..types import CensusData
from ..utils import LocaleData


@dataclasses.dataclass(frozen=True)
class CurrencyData(Ps2Data):
    """Data class for :class:`auraxium.ps2.currency.Currency`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    currency_id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'CurrencyData':
        return cls(
            int(data['currency_id']),
            LocaleData.from_census(data['name']),
            int(data['icon_id']),
            int(data['inventory_cap']))


class Currency(Cached, cache_size=10, cache_ttu=3600.0):
    """A currency obtainable by characters."""

    collection = 'currency'
    data: CurrencyData
    id_field = 'currency_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> CurrencyData:
        return CurrencyData.from_census(data)
