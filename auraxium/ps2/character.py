"""Objects related to characters."""

import logging
from typing import Awaitable, ClassVar, Final, Optional, Union

from ..base import Named
from ..cache import TLRUCache
from ..census import Query
from ..client import Client
from ..request import extract_single, run_query
from ..types import CensusData
from .faction import Faction

__all__ = ['Character']

log = logging.getLogger('auraxium.ps2')


class Character(Named, cache_size=256, cache_ttu=300.0):
    """A player-controlled character."""

    _cache: ClassVar[TLRUCache[Union[int, str], 'Character']]
    _collection = 'character'
    _id_field = 'character_id'

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
        COLLECTION = Final['single_character_by_id']
        log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('<%s:%d> not cached, generating API query...',
                  cls.__name__, id_)
        query = Query(collection=COLLECTION, service_id=client.service_id)
        query.add_term(field=cls._id_field, value=id_).limit(1)
        data = await run_query(query, session=client.session)
        payload = extract_single(data, COLLECTION)
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
        COLLECTION = Final['character']
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(f'_{name.lower()}')) is not None:
            log.debug('%r restored from cache', instance)
            return instance
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(collection=COLLECTION, service_id=client.service_id)
        query.add_term(field='name.first_lower', value=name.lower())
        data = await run_query(query, session=client.session)
        payload = extract_single(data, COLLECTION)
        return cls(payload, client=client)

    def name(self, locale: str = 'en') -> str:
        """Return the unique name of the player.

        Since character names are not localised, the "locale" kwarg is
        ignored.

        This will always return the capitalised version of the name.
        Use the built-int str.lower() method for a lowercase version.
        """
        return str(self._data['name']['first'])

    @staticmethod
    def _check_payload(payload: CensusData) -> CensusData:
        data = {}
        data['name'] = payload.pop('name')['first_lower']
        data['faction_id'] = payload.pop('faction_id')
        data['head_id'] = payload.pop('head_id')
        data['title_id'] = payload.pop('title_id')
        data['profile_id'] = payload.pop('profile_id')
        data['prestige_level'] = payload.pop('prestige_level')
        times = payload['times']
        data['times'] = {
            'creation': times.pop('creation'),
            'last_save': times.pop('last_save'),
            'last_login': times.pop('last_login'),
            'login_count': times.pop('login_count'),
            'minutes_played': times.pop('minutes_played')}
        certs = payload['certs']
        data['certs'] = {
            'earned_points': certs.pop('earned_points'),
            'gifted_points': certs.pop('gifted_points'),
            'spent_points': certs.pop('spent_points'),
            'available_points': certs.pop('available_points'),
            'percent_to_next': certs.pop('percent_to_next')}
        battle_rank = payload['battle_rank']
        data['battle_rank'] = {
            'value': battle_rank.pop('value'),
            'percent_to_next': battle_rank.pop('percent_to_next')}
        daily_ribbon = payload['daily_ribbon']
        data['daily_ribbon'] = {
            'count': daily_ribbon.pop('count'),
            'time': daily_ribbon.pop('time')}
        if not times:
            del data['times']
        if not certs:
            del data['certs']
        if not battle_rank:
            del data['battle_rank']
        if not daily_ribbon:
            del data['daily_ribbon']
        return data
