"""Character class definition."""

import dataclasses
import logging
from typing import ClassVar, Final, NamedTuple, Optional, Union

from ..base import Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
from ..client import Client
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_single, run_query
from ..types import CensusData
from ..utils import optional

from .faction import Faction
from .item import Item

log = logging.getLogger('auraxium.ps2')


@dataclasses.dataclass(frozen=True)
class CharacterData(Ps2Data):
    """Data class for :class:`auraxium.ps2.character.Character`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    class BattleRank(NamedTuple):
        """Object representation of the "battle_rank" sub-key."""

        value: int
        percent_to_next: float

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.BattleRank':
            return cls(
                int(data['value']),
                float(data['percent_to_next']))

    class Certs(NamedTuple):
        """Object representation of the "certs" sub-key."""

        earned_points: int
        gifted_points: int
        spent_points: int
        available_points: int
        percent_to_next: float

        @classmethod
        def from_census(cls, data: CensusData
                        ) -> 'CharacterData.Certs':
            return cls(
                int(data['earned_points']),
                int(data['gifted_points']),
                int(data['spent_points']),
                int(data['available_points']),
                float(data['percent_to_next']))

    class DailyRibbon(NamedTuple):
        """Object representation of the "daily_ribbon" sub-key."""

        count: int  # type: ignore
        time: Optional[int]
        date: Optional[str]

        @classmethod
        def from_census(cls, data: CensusData
                        ) -> 'CharacterData.DailyRibbon':
            return cls(
                int(data['count']),
                optional(data, 'time', int),
                optional(data, 'date', str))

    class Name(NamedTuple):
        """Object representation of the "name" sub-key."""

        first: str
        first_lower: str

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.Name':
            return cls(
                data['first'],
                data['first_lower'])

    class Times(NamedTuple):
        """Object representation of the "times" sub-key."""

        creation: int
        creation_date: str
        last_save: int
        last_save_date: str
        last_login: int
        last_login_date: str
        login_count: int
        minutes_played: int

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.Times':
            return cls(
                int(data['creation']),
                str(data['creation_date']),
                int(data['last_save']),
                str(data['last_save_date']),
                int(data['last_login']),
                str(data['last_login_date']),
                int(data['login_count']),
                int(data['minutes_played']))

    character_id: int
    name: Name
    faction_id: int
    head_id: int
    title_id: int
    times: Times
    certs: Certs
    battle_rank: BattleRank
    profile_id: int
    daily_ribbon: DailyRibbon
    prestige_level: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'CharacterData':
        return cls(
            int(data['character_id']),
            cls.Name.from_census(data['name']),
            int(data['faction_id']),
            int(data['head_id']),
            int(data['title_id']),
            cls.Times.from_census(data['times']),
            cls.Certs.from_census(data['certs']),
            cls.BattleRank.from_census(data['battle_rank']),
            int(data['profile_id']),
            cls.DailyRibbon.from_census(data['daily_ribbon']),
            int(data['prestige_level']))


class Character(Named, cache_size=256, cache_ttu=30.0):
    """A player-controlled fighter."""

    _cache: ClassVar[TLRUCache[Union[int, str], 'Character']]
    _collection = 'character'
    data: CharacterData
    _id_field = 'character_id'

    def _build_dataclass(self, data: CensusData) -> CharacterData:
        return CharacterData.from_census(data)

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction of the character.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query('faction', service_id=self._client.service_id,
                      faction_id=self.data.faction_id)
        proxy: InstanceProxy[Faction] = InstanceProxy(
            Faction, query, client=self._client)
        return proxy

    @classmethod
    async def get_by_id(cls, id_: int, *, client: Client
                        ) -> Optional['Character']:
        """Retrieve a character by their unique ID."""
        collection: Final[str] = 'single_character_by_id'
        log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('<%s:%d> not cached, generating API query...',
                  cls.__name__, id_)
        query = Query(collection, service_id=client.service_id,
                      character_id=id_).limit(1)
        data = await run_query(query, session=client.session)
        payload = extract_single(data, collection)
        return cls(payload, client=client)

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en', client: Client
                          ) -> Optional['Character']:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        """
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(f'_{name.lower()}')) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(cls._collection, service_id=client.service_id,
                      name__first_lower=name.lower()).limit(1)
        data = await run_query(query, session=client.session)
        payload = extract_single(data, cls._collection)
        return cls(payload, client=client)

    def items(self) -> SequenceProxy[Item]:
        """Return the items available to the character.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = self.query()
        join = query.create_join('characters_item').set_list(True)
        join.parent_field = join.child_field = 'character_id'
        inner = join.create_join('item')
        inner.parent_field = inner.child_field = 'item_id'
        proxy: SequenceProxy[Item] = SequenceProxy(
            Item, query, client=self._client)
        return proxy

    async def is_online(self) -> bool:
        """Return whether the given character is online."""
        collection: Final[str] = 'characters_online_status'
        query = Query(collection, character_id=self.id)
        payload = await run_query(query, session=self._client.session)
        data = extract_single(payload, collection)
        return bool(data['online_status'])

    def name(self, locale: str = 'en') -> str:
        """Return the unique name of the player.

        Since character names are not localised, the "locale" keyword
        argument is ignored.

        This will always return the capitalised version of the name.
        Use the built-int str.lower() method for a lowercase version.
        """
        return str(self.data.name.first)
