"""Defines the main client for Auraxium.

This includes both the core methods used to interface with the REST
API, as well as the websocket client used to access the real-time event
streaming service (ESS).
"""

import logging
import warnings
from typing import Any, Callable, List, Type, TypeVar, cast

from .base import Named, Ps2Object
from .census import Query
from .errors import NotFoundError, PayloadError
from .ps2 import Character, World
from ._rest import RequestClient, extract_payload, extract_single
from .types import CensusData

__all__ = [
    'Client'
]

_NamedT = TypeVar('_NamedT', bound=Named)
_Ps2ObjectT = TypeVar('_Ps2ObjectT', bound=Ps2Object)
_log = logging.getLogger('auraxium.client')


class Client(RequestClient):
    """The main client used to interface with the PlanetSide 2 API.

    This class handles access to the REST API at
    https://census.daybreakgames.com/.

    To interface with the REST API, use the methods :meth:`get`,
    :meth:`find`, or one of the ``Client.get_by_*()`` helpers.

    .. attribute:: loop
       :type: asyncio.AbstractEventLoop

       The :mod:`asyncio` event loop used by the client.

    .. attribute:: service_id
       :type: str

       The service ID identifying your app to the API. You can use the
       default value of ``'s:example'``, but you will likely run into
       rate limits. You can sign up for your own service ID at
       http://census.daybreakgames.com/#devSignup.

    .. attribute:: session
       :type: aiohttp.ClientSession

       The :class:`aiohttp.ClientSession` used for REST API requests.
    """

    async def count(self, type_: Type[Ps2Object], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        :param type_: The object type to search for.
        :type type_: type[auraxium.base.Ps2Object]
        :param kwargs: Any number of filters to apply.
        :return: The number of entries entries.
        """
        query = Query(type_.collection, service_id=self.service_id, **kwargs)
        result = await self.request(query, verb='count')
        try:
            return int(str(result['count']))
        except KeyError as err:  # pragma: no cover
            raise PayloadError(
                'Missing key "count" in API response', result) from err
        except ValueError as err:  # pragma: no cover
            raise PayloadError(
                f'Invalid count: {result["count"]}', result) from err

    async def find(self, type_: Type[_Ps2ObjectT], results: int = 10,
                   offset: int = 0, promote_exact: bool = False,
                   check_case: bool = True, **kwargs: Any) -> List[_Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        :param type_: The object type to search for.
        :type type_: type[auraxium.base.Ps2Object]
        :param int results: The maximum number of results.
        :param int offset: The number of entries to skip. Useful for
           paginated views.
        :param bool promote_exact: If enabled, exact matches to
           non-exact searches will always come first in the return
           list.
        :param bool check_case: Whether to check case when comparing
           strings. Note that case-insensitive searches are much more
           expensive.
        :param kwargs: Any number of filters to apply.
        :return: A list of matching entries.
        """
        query = Query(type_.collection, service_id=self.service_id, **kwargs)
        query.limit(results)
        if offset > 0:
            query.offset(offset)
        query.exact_match_first(promote_exact).case(check_case)
        matches = await self.request(query)
        return [type_(i, client=self) for i in extract_payload(
            matches, type_.collection)]

    async def get(self, type_: Type[_Ps2ObjectT], check_case: bool = True,
                  **kwargs: Any) -> _Ps2ObjectT | None:
        """Return the first entry matching the given terms.

        Like :meth:`Client.find`, but will only return one item.

        :param type_: The object type to search for.
        :type type_: type[auraxium.base.Ps2Object]
        :param bool check_case: Whether to check case when comparing
           strings. Note that case-insensitive searches are much more
           expensive.
        :param kwargs: Any number of filters to apply.
        :return: The first matching entry, or :obj:`None` if not found.
        """
        data = await self.find(
            type_, results=1, check_case=check_case, **kwargs)
        if data:
            if not isinstance(data[0], type_):
                raise RuntimeError(  # pragma: no cover
                    f'Expected {type_} instance, got {type(data[0])} instead, '
                    'please report this bug to the project maintainers')
            if len(data) > 1:
                warnings.warn(f'Ps2Object.get() got {len(data)} results, all '
                              'but the first will be discarded')
            return data[0]
        return None

    async def get_by_id(self, type_: Type[_Ps2ObjectT], id_: int
                        ) -> _Ps2ObjectT | None:
        """Retrieve an object by its unique Census ID.

        Like :meth:`Client.get`, but checks the local cache before
        performing the query.

        :param type_: The object type to search for.
        :type type_: type[auraxium.base.Ps2Object]
        :param int id_: The unique ID of the object.
        :return: The entry with the matching ID, or :obj:`None` if not
           found.
        """
        filters: dict[str, Any] = {type_.id_field: id_}
        data = await self.find(type_, results=1, **filters)
        if data and not isinstance(data[0], type_):
            raise RuntimeError(  # pragma: no cover
                f'Expected {type_} instance, got {type(data[0])} instead, '
                'please report this bug to the project maintainers')
        if data:
            return data[0]
        hook: Callable[[int], CensusData] | None
        if (hook := getattr(type_, 'fallback_hook', None)) is not None:
            try:
                fallback = hook(id_)
            except KeyError:
                _log.debug(
                    'No matching fallback instance found for ID %d', id_)
                return None
            _log.debug('Instantiating "%s" with ID %d through local copy',
                       type_.__name__, id_)
            return type_(fallback, client=self)
        return None

    async def get_by_name(self, type_: Type[_NamedT], name: str, *,
                          locale: str = 'en') -> _NamedT | None:
        """Retrieve an object by its unique name.

        Depending on the `type_` specified, this may retrieve a cached
        object, rather than querying the API.

        Keep in mind that not all :class:`~auraxium.base.Named` objects
        have a localised name; the `locale` argument has no effect in
        these cases.

        This query is always case-insensitive.

        :param type_: The object type to search for.
        :type type_: type[auraxium.base.Ps2Object]
        :param str name: The name to search for.
        :param str locale: The locale of the search key.
        :return: The entry with the matching name, or :obj:`None` if
           not found.
        """
        key = f'{locale}_{name.lower()}'
        _log.debug('%s "%s"[%s] requested', type_.__name__, name, locale)
        # pylint: disable=protected-access
        if (instance := type_._cache.get(key)) is not None:  # type: ignore
            _log.debug('%r restored from cache', instance)
            return instance
        _log.debug('%s "%s"[%s] not cached, generating API query...',
                   type_.__name__, name, locale)
        query = Query(type_.collection, service_id=self.service_id)
        if issubclass(type_, Character):
            query.add_term(field='name.first_lower', value=name.lower())
        elif issubclass(type_, World):
            return cast(_NamedT, await self._get_world_by_name(name, locale))
        else:
            query.case(False).add_term(field=f'name.{locale}', value=name)
        payload = await self.request(query)
        try:
            payload = extract_single(payload, type_.collection)
        except NotFoundError:  # pragma: no cover
            return None
        return cast(_NamedT, type_(payload, locale=locale, client=self))

    async def _get_world_by_name(self, name: str, locale: str = 'en',
                                 ) -> World | None:
        all_worlds = await self.find(World, results=100)
        for world in all_worlds:
            if getattr(world.name, locale).lower() == name.lower():
                return world
        return None
