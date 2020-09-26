"""Currency class definition."""

from ..base import Cached
from ..models import CurrencyData
from ..types import CensusData


class Currency(Cached, cache_size=10, cache_ttu=3600.0):
    """A currency obtainable by characters."""

    collection = 'currency'
    data: CurrencyData
    id_field = 'currency_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> CurrencyData:
        return CurrencyData.from_census(data)
