"""Outfit and outfit member class definitions."""

import dataclasses
import logging
from typing import ClassVar, Final, List, Optional, TYPE_CHECKING, Union

from ..base import Cached, Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
from ..client import Client
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload, extract_single
from ..types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the
    # 'Character' forward reference. This avoids a circular import at runtime.
    from .character import Character

log = logging.getLogger('auraxium.ps2')


@dataclasses.dataclass(frozen=True)
class OutfitMemberData(Ps2Data):
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'OutfitMemberData':
        return cls(
            int(data['outfit_id']),
            int(data['character_id']),
            int(data['member_since']),
            str(data['member_since_date']),
            str(data['rank']),
            int(data['rank_ordinal']))


class OutfitMember(Cached, cache_size=100, cache_ttu=300.0):
    """A member of an outfit.

    This class can be treated as an extension of the
    :class:`auraxium.ps2.character.Character` class.
    """

    collection = 'outfit_member'
    data: OutfitMemberData
    id_field = 'character_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> OutfitMemberData:
        return OutfitMemberData.from_census(data)

    def character(self) -> InstanceProxy['Character']:
        """Return the character associated with this member.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        # NOTE: This is required due to OutfitMember effectively being an
        # extension of Character.
        # pylint: disable=import-outside-toplevel
        from .character import Character
        query = Query(Character.collection, service_id=self._client.service_id)
        query.add_term(field=Character.id_field, value=self.data.character_id)
        return InstanceProxy(Character, query, client=self._client)

    def outfit(self) -> InstanceProxy['Outfit']:
        """Return the character associated with this member.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Outfit.collection, service_id=self._client.service_id)
        query.add_term(field=Outfit.id_field, value=self.data.outfit_id)
        return InstanceProxy(Outfit, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class OutfitRankData(Ps2Data):
    """Data class for :class:`auraxium.ps2.outfit.OutfitRank`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    outfit_id: int
    ordinal: int
    name: str
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'OutfitRankData':
        return cls(
            int(data['outfit_id']),
            int(data['ordinal']),
            str(data['name']),
            str(data['description']))


@dataclasses.dataclass(frozen=True)
class OutfitData(Ps2Data):
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

    @classmethod
    def from_census(cls, data: CensusData) -> 'OutfitData':
        return cls(
            int(data['outfit_id']),
            str(data['name']),
            str(data['name_lower']),
            str(data['alias']),
            str(data['alias_lower']),
            int(data['time_created']),
            str(data['time_created_date']),
            int(data['leader_character_id']),
            int(data['member_count']))


class Outfit(Named, cache_size=20, cache_ttu=300.0):
    """A player-run outfit."""

    _cache: ClassVar[TLRUCache[Union[int, str], 'Outfit']]
    collection = 'outfit'
    data: OutfitData
    id_field = 'outfit_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> OutfitData:
        return OutfitData.from_census(data)

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en', client: Client
                          ) -> Optional['Outfit']:
        """Retrieve an outfit by its unique name.

        This query is always case-insensitive.

        """
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(f'_{name.lower()}')) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(cls.collection, service_id=client.service_id,
                      name_lower=name.lower()).limit(1)
        data = await client.request(query)
        payload = extract_single(data, cls.collection)
        return cls(payload, client=client)

    @classmethod
    async def get_by_tag(cls, tag: str, client: Client) -> Optional['Outfit']:
        """Return an outfit by its unique tag.

        This query is always case-insensitive.

        """
        log.debug('%s with tag "%s" requested, generating API query...',
                  cls.__name__, tag)
        query = Query(cls.collection, service_id=client.service_id,
                      alias_lower=tag.lower()).limit(1)
        data = await client.request(query)
        payload = extract_single(data, cls.collection)
        return cls(payload, client=client)

    def leader(self) -> InstanceProxy[OutfitMember]:
        """Return the current leader of the outfit.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            OutfitMember.collection, service_id=self._client.service_id)
        query.add_term(
            field=OutfitMember.id_field, value=self.data.leader_character_id)
        return InstanceProxy(OutfitMember, query, client=self._client)

    def members(self) -> SequenceProxy[OutfitMember]:
        """Return the members of the outfit.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            OutfitMember.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(5000)
        return SequenceProxy(OutfitMember, query, client=self._client)

    def name(self, locale: str = 'en') -> str:
        """Return the unique name of the outfit.

        Since outfit names are not localised, the "locale" keyword
        argument is ignored.

        This will always return the capitalised version of the name.
        Use the built-int str.lower() method for a lowercase version.
        """
        return str(self.data.name)

    async def ranks(self) -> List[OutfitRankData]:
        """Return the list of ranks for the outfit."""
        collection: Final[str] = 'outfit_rank'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        data = await self._client.request(query)
        payload = extract_payload(data, collection)
        return [OutfitRankData.from_census(c) for c in payload]
