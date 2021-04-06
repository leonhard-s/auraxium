"""Data classes for :mod:`auraxium.ps2.outfit`."""

from ._base import RESTPayload

__all__ = [
    'OutfitData',
    'OutfitMemberData',
    'OutfitRankData'
]

# pylint: disable=too-few-public-methods


class OutfitData(RESTPayload):
    """Data class for :class:`auraxium.ps2.outfit.Outfit`.

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
    """Data class for :class:`auraxium.ps2.outfit.OutfitMember`.

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
    """Data class for :class:`auraxium.ps2.outfit.OutfitRank`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    outfit_id: int
    ordinal: int
    name: str
    description: str
