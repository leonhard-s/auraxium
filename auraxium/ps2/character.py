"""Character class definition."""

import dataclasses
import logging
from typing import (Any, ClassVar, Final, List, NamedTuple, Optional, Tuple,
                    Union)

from ..base import Named, Ps2Data
from ..cache import TLRUCache
from ..census import Query
from ..client import Client
from ..errors import NotFoundError
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload, extract_single
from ..types import CensusData
from ..utils import LocaleData, optional

from .faction import Faction
from .item import Item
from .outfit import Outfit, OutfitMember
from .profile import Profile
from .world import World

log = logging.getLogger('auraxium.ps2')


class CharacterAchievement(NamedTuple):
    """Data container for a character's achievement status.

    Attributes:
        character_id: The ID of the character for this entry.
        achievement_id: The ID of the achievement for this entry.
        earned_count: How often the character has earned the given
            achievement.
        start: The UTC timestamp the character started progression
            towards this achievement at.
        start_date: Human-readable version of :attr:`start`.
        finish: The time the character completed this achievement. Only
            valid for one-time achievements such as medals.
        finish_date: Human-readable version of :attr:`finish`.
        last_save: The last time the character gained this
            achievement at as a UTC timestamp.
        last_save_date: Human-readable version of :attr:`last_save`.

        """

    character_id: int
    achievement_id: int
    earned_count: int
    start: int
    start_date: str
    finish: int
    finish_date: str
    last_save: int
    last_save_date: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'CharacterAchievement':
        """Populate the data class with values from the dictionary.

        This parses the API response and casts the appropriate types.
        """
        return cls(
            int(data['character_id']),
            int(data['achievement_id']),
            int(data['earned_count']),
            int(data['start']),
            str(data['start_date']),
            int(data['finish']),
            str(data['finish_date']),
            int(data['last_save']),
            str(data['last_save_date']))


class CharacterDirective(NamedTuple):
    """Data container for a character's directive status.
    
    Attributes:
        character_id: The ID of the character for this entry.
        directive_tree_id: The ID of the directive tree for this entry.
        directive_id: The ID of the directive for this entry.
        completion_time: The time the character completed this
            directive.
        completion_time_date: Human-readable version of
            :attr:`completion_time`.
            
    """

    character_id: int
    directive_tree_id: int
    directive_id: int
    completion_time: int
    completion_time_date: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'CharacterDirective':
        """Populate the data class with values from the dictionary.

        This parses the API response and casts the appropriate types.
        """
        return cls(
            int(data['character_id']),
            int(data['directive_tree_id']),
            int(data['directive_id']),
            int(data['completion_time']),
            str(data['completion_time_date']))


@dataclasses.dataclass(frozen=True)
class TitleData(Ps2Data):
    """Data class for :class:`auraxium.ps2.character.Title`.

    .. important::
        Unlike most other forms of API data, the ID used by titles is
        **not** unique.

        This is due to the ASP system re-using the same title IDs while
        introducing a different name ("A.S.P. Operative" for ``en``).

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        title_id: The ID of this title.
        name: The localised name of this title.

    """

    title_id: int
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'TitleData':
        return cls(
            int(data['title_id']),
            LocaleData.from_census(data['name']))


class Title(Named, cache_size=300, cache_ttu=300.0):
    """A title selectable by a character."""

    collection = 'title'
    data: TitleData
    id_field = 'title_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> TitleData:
        return TitleData.from_census(data)


@dataclasses.dataclass(frozen=True)
class CharacterData(Ps2Data):
    """Data class for :class:`auraxium.ps2.character.Character`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        character_id: The unique name of the character.
        name: The name of the player.
        faction_id: The faction the character belongs to.
        head_id: The head model for this character.
        title_id: The current title selected for this character. May be
            zero.
        times: Play and login time data for the character.
        certs: Certification data for the character.
        battle_rank: Battle rank data for the character.
        profile_id: The last profile the character used.
        daily_ribbon: Daily ribbon data for the character.
        prestige_level: The ASP rank of the character.

    """

    class BattleRank(NamedTuple):
        """Object representation of the "battle_rank" sub-key.

        Attributes:
            value: The current battle rank.
            percent_to_next: The progress to the next battle rank.

        """

        value: int
        percent_to_next: float

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.BattleRank':
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
            return cls(
                int(data['value']),
                float(data['percent_to_next']))

    class Certs(NamedTuple):
        """Object representation of the "certs" sub-key.

        Attributes:
            earned_points: Certification points the player has ever
                earned.
            gifted_points: Certification points the player was gifted
                through events.
            spent_points: Certification points the character has spent.
            available_points: The current certification point balance
                of the character.
            percent_to_next: The progress to the next certification
                point for the character.

            """

        earned_points: int
        gifted_points: int
        spent_points: int
        available_points: int
        percent_to_next: float

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.Certs':
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
            return cls(
                int(data['earned_points']),
                int(data['gifted_points']),
                int(data['spent_points']),
                int(data['available_points']),
                float(data['percent_to_next']))

    class DailyRibbon(NamedTuple):
        """Object representation of the "daily_ribbon" sub-key.

        Attributes:
            count: The number of daily ribbon bonuses available.
            time: (Not yet documented)
            date: Human-readable version of :attr:`time`.

        """

        count: int  # type: ignore
        time: Optional[int]
        date: Optional[str]

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.DailyRibbon':
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
            return cls(
                int(data['count']),
                optional(data, 'time', int),
                optional(data, 'date', str))

    class Name(NamedTuple):
        """Object representation of the "name" sub-key.
        
        Attributes:
            first: The name of the character.
            first_lower: Lowercase version of :attr:`first`.
        
        """

        first: str
        first_lower: str

        @classmethod
        def from_census(cls, data: CensusData) -> 'CharacterData.Name':
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
            return cls(
                data['first'],
                data['first_lower'])

    class Times(NamedTuple):
        """Object representation of the "times" sub-key.
        
        Attributes:
            creation: The time the character was created.
            creation_date: Human-readable version of :attr:`creation`.
            last_save: The last time the character was updated. This
                roughly matches the last time the character logged out.
            last_save_date: Human-readable version of
                :attr:`last_save`.
            last_login: The last time the character logged in.
            last_login_date: Human-readable version of
                :attr:`last_login_date`.
            login_count: The number of times the character has logged
                in.
            minutes_played: The total number of minutes this character
                was logged into PS2.
            
            """

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
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
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
    collection = 'character'
    data: CharacterData
    id_field = 'character_id'

    async def achievements(self, **kwargs: Any) -> List[CharacterAchievement]:
        """Return the achievement status for a character."""
        collection: Final[str] = 'characters_achievement'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.limit(5000)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return [CharacterAchievement.from_census(d) for d in data]

    @staticmethod
    def _build_dataclass(data: CensusData) -> CharacterData:
        return CharacterData.from_census(data)

    async def currency(self) -> Tuple[int, int]:
        """Return the currencies of the character.

        This returns a tuple of the number of Nanites and ASP tokens
        available to the player.

        Other currencies are not exposed to the API as of the writing
        of this module.
        """
        collection: Final[str] = 'characters_currency'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        return int(data['quantity']), int(data['prestige_currency'])

    async def directive(self, results: int = 1,
                        **kwargs: Any) -> List[CensusData]:
        """Query the directive status for this character."""
        collection: Final[str] = 'characters_directive'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def directive_objective(self, results: int = 1,
                                  **kwargs: Any) -> List[CensusData]:
        """Query the objective status for a directive."""
        collection: Final[str] = 'characters_directive_objective'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def directive_tier(self, results: int = 1,
                             **kwargs: Any) -> List[CensusData]:
        """Query the directive tier status for this character."""
        collection: Final[str] = 'characters_directive_tier'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def directive_tree(self, results: int = 1,
                             **kwargs: Any) -> List[CensusData]:
        """Query the directive tree status for this character."""
        collection: Final[str] = 'characters_directive_tree'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def events(self, **kwargs: Any) -> List[CensusData]:
        """Return and process past events for this character.

        This provides a REST endpoint for past character events.

        This is always limited to at most 1000 return values. Use the
        begin and end parameters to poll more data.
        """
        collection: Final[str] = 'characters_event'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(1000)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection=collection)
        return data

    async def events_grouped(self, **kwargs: Any) -> List[CensusData]:
        """Used to obtain kills and deaths on a per-player basis."""
        collection: Final[str] = 'characters_event_grouped'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100_000)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection=collection)
        return data

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction of the character.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    async def friends(self) -> List['Character']:
        """Return the friends list of the character."""
        # NOTE: Due to the strange formatting of the characters_friend
        # collection, I does not seem possible to retrieve the associated
        # characters through joins.
        # This is solved through a second query matching the IDs, though this
        # does slow this query down dramatically.
        collection: Final[str] = 'characters_friend'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Character.id_field, value=self.id)
        join = query.create_join(self.collection)
        join.set_list(True)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        character_ids: List[str] = [
            str(d['character_id']) for d in data['friend_list']]
        characters = await Character.find(
            results=len(character_ids), client=self._client,
            character_id=','.join(character_ids))
        return characters

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
        data = await client.request(query)
        try:
            payload = extract_single(data, collection)
        except NotFoundError:
            return None
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
        query = Query(cls.collection, service_id=client.service_id,
                      name__first_lower=name.lower()).limit(1)
        data = await client.request(query)
        try:
            payload = extract_single(data, cls.collection)
        except NotFoundError:
            return None
        return cls(payload, client=client)

    @classmethod
    async def get_online(cls, id_: int, *args: int, client: Client
                         ) -> List['Character']:
        """Retrieve the characters that are online from a list."""
        char_ids = [id_]
        char_ids.extend(args)
        log.debug('Retrieving online status for %s characters', len(char_ids))
        query = Query(cls.collection, service_id=client.service_id,
                      character_id=','.join(str(c) for c in char_ids))
        query.limit(len(char_ids)).resolve('online_status')
        data = await client.request(query)
        payload = extract_payload(data, cls.collection)
        return [cls(c, client=client) for c in payload
                if int(c['online_status'])]

    def items(self) -> SequenceProxy[Item]:
        """Return the items available to the character.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'characters_item'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(5000)
        join = query.create_join(Item.collection)
        join.parent_field = join.child_field = Item.id_field
        return SequenceProxy(Item, query, client=self._client)

    async def is_online(self) -> bool:
        """Return whether the given character is online."""
        return bool(int(await self.online_status()))

    def name(self, locale: str = 'en') -> str:
        """Return the unique name of the player.

        Since character names are not localised, the "locale" keyword
        argument is ignored.

        This will always return the capitalised version of the name.
        Use the built-int str.lower() method for a lowercase version.
        """
        return str(self.data.name.first)

    async def name_long(self) -> str:
        """Return the full name of the player.

        This includes an optional player title if the player has
        selected one.
        """
        if (title := await self.title()) is not None:
            return f'{title.name()} {self.name()}'
        return self.name()

    async def online_status(self) -> int:
        """Return the online status of the character.

        This returns 0 if the character is offline, or the world_id of
        the server they are logged into.
        """
        collection: Final[str] = 'characters_online_status'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        payload = await self._client.request(query)
        data = extract_single(payload, collection)
        return int(data['online_status'])

    def outfit(self) -> InstanceProxy[Outfit]:
        """Return the outfit of the character, if any.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        collection: Final[str] = 'outfit_member_extended'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        return InstanceProxy(Outfit, query, client=self._client)

    def outfit_member(self) -> InstanceProxy[OutfitMember]:
        """Return the outfit member of the character, if any.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(
            OutfitMember.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        return InstanceProxy(OutfitMember, query, client=self._client)

    def profile(self) -> InstanceProxy[Profile]:
        """Return the last played profile of the character.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Profile.collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        return InstanceProxy(Profile, query, client=self._client)

    async def skill(self, results: int = 1, **kwargs: Any) -> List[CensusData]:
        """Return the skills unlocked by this character."""
        collection: Final[str] = 'characters_skill'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def stat(self, results: int = 1, **kwargs: Any) -> List[CensusData]:
        """Return global statistics for this character."""
        collection: Final[str] = 'characters_skill'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def stat_by_faction(self, results: int = 1,
                              **kwargs: Any) -> List[CensusData]:
        """Return faction-specific statistics for this character."""
        collection: Final[str] = 'characters_stat_by_faction'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def stat_history(self, results: int = 1,
                           **kwargs: Any) -> List[CensusData]:
        """Return historical statistics for this character."""
        collection: Final[str] = 'characters_stat_history'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def weapon_stat(self, results: int = 1,
                          **kwargs: Any) -> List[CensusData]:
        """Return weapon-specific statistics for this character."""
        collection: Final[str] = 'characters_weapon_stat'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    async def weapon_stat_by_faction(self, results: int = 1,
                                     **kwargs: Any) -> List[CensusData]:
        """Return per-faction weapon statistics for this character."""
        collection: Final[str] = 'characters_weapon_stat_by_faction'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(results)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        return data

    def title(self) -> InstanceProxy[Title]:
        """Return the current title of the character, if any.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        title_id = self.data.title_id or -1
        query = Query(Title.collection, service_id=self._client.service_id)
        query.add_term(field=Title.id_field, value=title_id)
        return InstanceProxy(Title, query, client=self._client)

    def world(self) -> InstanceProxy[World]:
        """Return the world of the character.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        collection: Final[str] = 'characters_world'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join(World.collection)
        join.parent_field = join.child_field = 'world_id'
        return InstanceProxy(World, query, client=self._client)
