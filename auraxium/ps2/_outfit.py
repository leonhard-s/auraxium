"""Outfit and outfit member class definitions."""

import logging
from typing import Any, ClassVar, Final, TYPE_CHECKING, cast

from ..base import Cached, Named, NamedT
from .._cache import TLRUCache
from ..census import Query
from ..errors import NotFoundError
from ..collections import OutfitData, OutfitMemberData, OutfitRankData
from .._proxy import InstanceProxy, SequenceProxy
from .._rest import RequestClient, extract_payload, extract_single
from .._support import deprecated

if TYPE_CHECKING:  # pragma: no cover
    # This is only imported during static type checking to resolve the
    # 'Character' forward reference. This avoids a circular import at runtime.
    from ._character import Character

__all__ = [
    'Outfit',
    'OutfitMember'
]

log = logging.getLogger('auraxium.ps2')


class OutfitMember(Cached, cache_size=100, cache_ttu=300.0):
    """A member of an outfit.

    This class can be treated as an extension of the
    :class:`~auraxium.ps2.Character` class.

    .. attribute:: outfit_id
       :type: int

       The ID of the outfit this member is a part of.

    .. attribute:: id
       :type: int

       The ID of the associated character. In the API payload, this
       field is called ``character_id``.

    .. attribute:: member_since
       :type: int

       The date the character joined the outfit at as a UTC timestamp.

    .. attribute:: member_since_date
       :type: str

       Human-readable version of :attr:`member_since`.

    .. attribute:: rank
       :type: str

       The name of the member's in-game outfit rank.

    .. attribute:: rank_ordinal
       :type: int

       The ordinal position of the member's rank within the outfit. The
       lower the value, the higher the rank.
    """

    collection = 'outfit_member'
    data: OutfitMemberData
    id_field = 'character_id'
    _model = OutfitMemberData

    # Type hints for data class fallback attributes
    outfit_id: int
    id: int
    member_since: int
    member_since_date: str
    rank: str
    rank_ordinal: int

    def character(self) -> InstanceProxy['Character']:
        """Return the character associated with this member.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        # NOTE: This is required due to OutfitMember effectively being an
        # extension of Character.
        # pylint: disable=import-outside-toplevel
        from ._character import Character
        query = Query(Character.collection, service_id=self._client.service_id)
        query.add_term(field=Character.id_field, value=self.data.character_id)
        return InstanceProxy(Character, query, client=self._client)

    def outfit(self) -> InstanceProxy['Outfit']:
        """Return the character associated with this member.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Outfit.collection, service_id=self._client.service_id)
        query.add_term(field=Outfit.id_field, value=self.data.outfit_id)
        return InstanceProxy(Outfit, query, client=self._client)


class Outfit(Named, cache_size=20, cache_ttu=300.0):
    """A player-run outfit.

    .. attribute:: id
       :type: int

       The unique ID of the outfit. In the API payload, this field is
       called ``outfit_id``.

    .. attribute:: name_lower
       :type: str

       Lowercase version of :attr:`name`. Useful for optimising
       case-insensitive lookups.

    .. attribute:: alias
       :type: str

       The alias (or tag) of the outfit.

    .. attribute:: alias_lower
       :type: str

       Lowercase version of :attr:`alias`. Useful for optimising
       case-insensitive lookups.

    .. attribute:: name
       :type: str

       Name of the outfit. Not localised.

    .. attribute:: time_created
       :type: int

       The creation date of the outfit as a UTC timestamp.

    .. attribute:: time_created_date
       :type: str

       Human-readable version of :attr:`time_created`.

    .. attribute:: leader_character_id
       :type: int

       The character/member ID of the outfit leader.

    .. attribute:: member_count
       :type: int

       The number of members in the outfit.
    """

    _cache: ClassVar[TLRUCache[int | str, 'Outfit']]
    collection = 'outfit'
    data: OutfitData
    id_field = 'outfit_id'
    _model = OutfitData

    # Type hints for data class fallback attributes
    id: int
    alias: str
    time_created: int
    time_created_date: str
    leader_character_id: int
    member_count: int
    name: str

    @property
    def tag(self) -> str:
        """Alias of :attr:`alias`."""
        return self.alias

    @classmethod
    @deprecated('0.2', '0.5', replacement=':meth:`auraxium.Client.get`')
    async def get_by_name(cls: type[NamedT], name: str, *, locale: str = 'en',
                          client: RequestClient
                          ) -> NamedT | None:  # pragma: no cover
        """Retrieve an outfit by its unique name.

        This query is always case-insensitive.
        """
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(f'_{name.lower()}')) is not None:
            log.debug('%r restored from cache', instance)
            return cast(NamedT, instance)
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(cls.collection, service_id=client.service_id,
                      name_lower=name.lower()).limit(1)
        data = await client.request(query)
        try:
            payload = extract_single(data, cls.collection)
        except NotFoundError:
            return None
        return cls(payload, client=client)

    @classmethod
    @deprecated('0.2', '0.5', replacement=':meth:`auraxium.Client.get`')
    async def get_by_tag(cls, tag: str, client: RequestClient
                         ) -> 'Outfit | None':  # pragma: no cover
        """Return an outfit by its unique tag.

        This query is always case-insensitive.
        """
        log.debug('%s with tag "%s" requested, generating API query...',
                  cls.__name__, tag)
        query = Query(cls.collection, service_id=client.service_id,
                      alias_lower=tag.lower()).limit(1)
        data = await client.request(query)
        try:
            payload = extract_single(data, cls.collection)
        except NotFoundError:
            return None
        return cls(payload, client=client)

    def leader(self) -> InstanceProxy[OutfitMember]:
        """Return the current leader of the outfit.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        assert self.data.leader_character_id is not None
        query = Query(
            OutfitMember.collection, service_id=self._client.service_id)
        query.add_term(
            field=OutfitMember.id_field, value=self.data.leader_character_id)
        return InstanceProxy(OutfitMember, query, client=self._client)

    def members(self) -> SequenceProxy[OutfitMember]:
        """Return the members of the outfit.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(
            OutfitMember.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(5000)
        return SequenceProxy(OutfitMember, query, client=self._client)

    async def ranks(self) -> list[OutfitRankData]:
        """Return the list of ranks for the outfit."""
        collection: Final[str] = 'outfit_rank'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        data = await self._client.request(query)
        payload = extract_payload(data, collection)
        return [OutfitRankData(**cast(Any, c)) for c in payload]
