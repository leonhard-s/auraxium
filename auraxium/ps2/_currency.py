"""Currency class definition."""

from ..base import Cached
from ..collections import CurrencyData
from ..types import LocaleData

__all__ = [
    'Currency'
]


class Currency(Cached, cache_size=10, cache_ttu=3600.0):
    """A currency obtainable by characters.

    .. note::

       As of April 2021, the only currency available are Nanites. None
       of the new player resources (A-7, Merit, Campaign Standing etc.)
       are available.

       The current A.S.P. token balance of a player can be retrieved
       through the :meth:`auraxium.ps2.Character.currency` method.

    .. attribute:: id
       :type: int

       The unique ID of this currency. In the API payload, this field
       is called ``currency_id``.

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
