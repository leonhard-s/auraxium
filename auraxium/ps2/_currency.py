"""Currency class definition."""

from ..base import Cached
from ..models import CurrencyData
from ..types import LocaleData

__all__ = [
    'Currency'
]


class Currency(Cached, cache_size=10, cache_ttu=3600.0):
    """A currency obtainable by characters.

    .. attribute:: id
       :type: int

       The unique ID of this currency entry.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       The localised name of this currency.

    .. attribute:: icon_id
       :type: int

       The image ID of the currency icon image asset.

    .. attribute:: inventory_cap
       :type: int

       The maximum amount of this currency a character may hold.
    """

    collection = 'currency'
    data: CurrencyData
    id_field = 'currency_id'
    _model = CurrencyData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    icon_id: int
    inventory_cap: int
