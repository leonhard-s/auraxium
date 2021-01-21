"""Utility functions for working with leaderboard data."""

import enum
import warnings
from typing import Dict, Final, List, Optional, Tuple, Union

from ..census import Query
from ..errors import NotFoundError
from ..client import Client
from .._request import extract_payload, extract_single

from .character import Character
from .world import World

__all__ = [
    'by_char',
    'by_char_multi',
    'Period',
    'Stat',
    'top'
]


class Period(enum.Enum):
    """The periods supported by the leaderboard."""

    FOREVER = 0
    MONTHLY = 1
    WEEKLY = 2
    DAILY = 3
    ONE_LIFE = 4


class Stat(enum.Enum):
    """A statistic tracked by the leaderboard."""

    KILLS = 0
    SCORE = 1
    TIME = 2
    DEATHS = 3


async def by_char(stat: Stat, character: Union[int, Character],
                  period: Period = Period.FOREVER,
                  *, client: Client) -> Optional[Tuple[int, int]]:
    """Return the rank of the player on the leaderboard.

    Note that only the top 10'000 players are tracked by the
    leaderboard. For characters not in the top 10'000, this will return
    None. Otherwise, this returns the a tuple consisting of the rank
    and stat value for the character.
    """
    char_id = character if isinstance(character, int) else character.id
    collection: Final[str] = 'characters_leaderboard'
    query = Query(collection, service_id=client.service_id)
    query.add_term(field=Character.id_field, value=char_id)
    query.add_term(field='name', value=_name_from_stat(stat))
    query.add_term(field='period', value=_period_from_enum(period))
    payload = await client.request(query)
    try:
        data = extract_single(payload, collection)
    except NotFoundError:
        return None
    return int(data['rank']), int(data['value'])


async def by_char_multi(stat: Stat, character: Union[int, Character],
                        *args: Union[int, Character],
                        period: Period = Period.FOREVER,
                        client: Client) -> List[Tuple[int, int]]:
    """Return the rank of the players on the leaderboard.

    Like by_char, but takes any number of arguments.
    """
    char_ids = [character if isinstance(character, int) else character.id]
    char_ids.extend([c if isinstance(c, int) else c.id for c in args])
    value = ','.join(str(c) for c in char_ids)
    collection: Final[str] = 'characters_leaderboard'
    query = Query(collection, service_id=client.service_id)
    query.add_term(field=Character.id_field, value=value)
    query.add_term(field='name', value=_name_from_stat(stat))
    query.add_term(field='period', value=_period_from_enum(period))
    payload = await client.request(query)
    data = extract_payload(payload, collection)
    return_: Dict[int, Tuple[int, int]] = {i: (-1, -1) for i in char_ids}
    for row in data:
        id_ = int(row['character_id'])
        return_[id_] = int(row['rank']), int(row['value'])
    return [return_[i] for i in char_ids]


async def top(stat: Stat, period: Period = Period.FOREVER, matches: int = 10,
              offset: int = 0, world: Optional[Union[int, World]] = None,
              *, client: Client) -> List[Tuple[int, Character]]:
    """Retrieve the top entries on the leaderboard for the given stat.

    Note that only the top 10'000 players are tracked by the
    leaderboard.
    """
    if matches > 10_000:
        warnings.warn('Results will been truncated to 10k elements due to '
                      'API limitations')
        matches = 10_000
    collection: Final[str] = 'leaderboard'
    query = Query(collection, service_id=client.service_id)
    query.add_term(field='name', value=_name_from_stat(stat))
    query.add_term(field='period', value=_period_from_enum(period))
    if world is not None:
        world_id: int = world if isinstance(world, int) else world.id
        query.add_term(field='world', value=world_id)
    query.limit(matches)
    query.start(offset)
    join = query.create_join(Character.collection)
    join.set_fields(Character.id_field)
    payload = await client.request(query)
    key = 'character_id_join_character'
    return [(int(d['value']), Character(d[key], client=client))
            for d in extract_payload(payload, collection=collection)]


def _name_from_stat(stat: Stat) -> str:
    periods = ['Kills', 'Score', 'Time', 'Deaths']
    return periods[stat.value]


def _period_from_enum(period: Period) -> str:
    names = ['Forever', 'Monthly', 'Weekly', 'Daily', 'OneLife']
    return names[period.value]
