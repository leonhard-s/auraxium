"""Data classes for :mod:`auraxium.ps2._outfit`."""

from .base import RESTPayload

__all__ = [
    'OutfitData',
    'OutfitMemberData',
    'OutfitRankData'
]


class OutfitData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Outfit`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    outfit_id: int
    name: str
    name_lower: str
    alias: str
    alias_lower: str
    time_created: int
    time_created_date: str
    leader_character_id: int
    member_count: int


class OutfitMemberData(RESTPayload):
    """Data class for :class:`auraxium.ps2.OutfitMember`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    outfit_id: int
    character_id: int
    member_since: int
    member_since_date: str
    rank: str
    rank_ordinal: int


class OutfitRankData(RESTPayload):
    """Data class for custom, outfit-specific ranks.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    .. attribute:: outfit_id
       :type: int

       The ID of the :class:`~auraxium.ps2.Outfit` that defined this
       rank.

    .. attribute:: ordinal
       :type: int

       The ordinal position of this rank in the outfit's roster. Lower
       values denote a higher rank.

    .. attribute:: name
       :type: str

       The custom name of the outfit rank.

    .. attribute:: description
       :type: str

       The description of the rank.
    """

    outfit_id: int
    ordinal: int
    name: str
    description: str
