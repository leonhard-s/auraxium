"""Objects related to characters."""

import logging
from typing import Awaitable, ClassVar, Final, Optional, Union

from ..base import Named
from ..cache import TLRUCache
from ..census import Query
from ..client import Client
from ..request import extract_single, run_query
from ..types import CensusInfo
from .faction import Faction

__all__ = ['Character']

log = logging.getLogger('auraxium.ps2')


class Character(Named, cache_size=256, cache_ttu=300.0):
    """A player-controlled character."""

    _cache: ClassVar[TLRUCache[Union[int, str], 'Character']]
    _collection = 'character'
    _id_field = 'character_id'

    _census_info = CensusInfo(
        # Census name to ARX name
        {'name.first': 'name',
         'name.first_lower': 'name_lower',
         'faction_id': 'faction_id',
         'title_id': 'title_id',
         'prestige_level': 'asp_rank',
         'times.creation': 'created',
         'times.last_save': 'last_seen',
         'times.last_login': 'last_login',
         'times.login_count': 'login_count',
         'times.minutes_played': 'playtime',
         'certs.available_points': 'certs',
         'certs.earned_points': 'certs_earned',
         'certs.gifted_points': 'certs_gifted',
         'certs.spent_points': 'certs_spent',
         'battle_rank.value': 'battle_rank',
         'battle_rank.percent_to_next': 'battle_rank_progress',
         'profile_id': 'profile_id',
         'daily_ribbon.count': 'daily_ribbons'},
        # Field names to exclude
        ['head_id', 'times.creation_date', 'times.last_save_date',
         'times.last_login_date', 'certs.percent_to_next',
         'daily_ribbon.time', 'daily_ribbon.date'],
        # Converter functions
        {'times.minutes_played': lambda x: x/60.0,
         'playtime': lambda x: int(x*60)})

    @property
    def faction(self) -> Awaitable[Faction]:
        """Return the faction of the player."""
        faction_id = int(self._data['faction_id'])
        faction = Faction.get_by_id(faction_id, client=self._client)
        return faction  # type: ignore

    @classmethod
    async def get_by_id(cls, id_: int, *, client: Client
                        ) -> Optional['Character']:
        """Retrieve an object by their unique Census ID.

        Args:
            id_: The unique ID of the character.
            client: The client through which to perform the request.

        Returns:
            The character with the matching ID, or None if not found.

        """
        table = Final['single_character_by_id']
        log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('<%s:%d> not cached, generating API query...',
                  cls.__name__, id_)
        query = Query(collection=table, service_id=client.service_id)
        query.add_term(field=cls._id_field, value=id_).limit(1)
        data = await run_query(query, session=client.session)
        payload = extract_single(data, table)
        return cls(payload, client=client)

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en', client: Client
                          ) -> Optional['Character']:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        Args:
            client: The client through which to perform the request.
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to 'en'.

        Returns:
            The entry with the matching name, or None if not found.

        """
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(f'_{name.lower()}')) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(collection=cls._collection, service_id=client.service_id)
        query.add_term(field='name.first_lower', value=name.lower())
        data = await run_query(query, session=client.session)
        payload = extract_single(data, cls._collection)
        return cls(payload, client=client)

    def name(self, locale: str = 'en') -> str:
        """Return the unique name of the player.

        Since character names are not localised, the "locale" kwarg is
        ignored.

        This will always return the capitalised version of the name.
        Use the built-int str.lower() method for a lowercase version.
        """
        return str(self._data['name'])
