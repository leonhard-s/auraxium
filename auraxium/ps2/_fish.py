"""Fishing class definitions."""

from ..base import ImageMixin, Named
from ..models import FishData
from ..types import LocaleData

__all__ = [
    'Fish',
]


class Fish(Named, ImageMixin, cache_size=32, cache_ttu=3600.0):
    """A fish that can be caught in the game.

    .. attribute:: id
       :type: int

       The unique ID of this fish. In the API payload, this field is
       called ``fish_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the fish.

    .. attribute:: rarity
        :type: int
    
        (Not yet documented)

    .. attribute:: average_size
        :type: int

        (Not yet documented)

    .. attribute:: size_deviation
        :type: int

        (Not yet documented)

    .. attribute:: scan_point_amount
        :type: int

        (Not yet documented)

    .. attribute:: cost
        :type: int

        (Not yet documented)
    """

    collection = 'fish'
    data: FishData
    id_field = 'fish_id'
    _model = FishData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    rarity: int
    average_size: int
    size_deviation: int
    scan_point_amount: int
    cost: int
