"""Defines the main client for Auraxium.

This includes both the core methods used to interface with the REST
API, as well as the websocket client used to access the real-time event
streaming service (ESS).

"""

import logging
import warnings
from typing import Any, Callable, List, Optional, Type, TypeVar, cast

from .base import Named, Ps2Object
from .census import Query
from .errors import NotFoundError, PayloadError
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
    ``https://census.daybreakgames.com/``.

    To interface with the REST API, use the methods :meth:`Client.get`,
    :meth:`Client.find()`, or one of the ``Client.get_by_*()`` helpers.

    Attributes:
        loop: The :mod:`asyncio` event loop used by the client.
        service_id: The service ID identifying your app to the API. You
            can use the default value of ``'s:example'``, but you will
            likely run into rate limits. You can sign up for your own
            service ID at http://census.daybreakgames.com/#devSignup.
        session: The :class:`aiohttp.ClientSession` used for REST API
            requests.

    """

    async def count(self, type_: Type[Ps2Object], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Arguments:
            type_: The object type to search for.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        query = Query(type_.collection, service_id=self.service_id, **kwargs)
        result = await self.request(query, verb='count')
        try:
            return int(cast(str, result['count']))
        except KeyError as err:
            raise PayloadError(
                'Missing key "count" in API response', result) from err
        except ValueError as err:
            raise PayloadError(
                f'Invalid count: {result["count"]}', result) from err

    async def find(self, type_: Type[_Ps2ObjectT], results: int = 10,
                   offset: int = 0, promote_exact: bool = False,
                   check_case: bool = True, **kwargs: Any) -> List[_Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Arguments:
            type_: The object type to search for.
            results (optional): The maximum number of results. Defaults
                to ``10``.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to ``0``.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to ``False``.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

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
                  **kwargs: Any) -> Optional[_Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like :meth:`Client.find()`, but will only return one item.

        Arguments:
            type_: The object type to search for.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to ``True``.
            **kwargs: Any number of filters to apply.

        Returns:
            The first matching entry, or ``None`` if not found.

        """
        data = await self.find(
            type_, results=1, check_case=check_case, **kwargs)
        if data:
            if not isinstance(data[0], type_):
                raise RuntimeError(
                    f'Expected {type_} instance, got {type(data[0])} instead, '
                    'please report this bug to the project maintainers')
            if len(data) > 1:
                warnings.warn(f'Ps2Object.get() got {len(data)} results, all '
                              'but the first will be discarded')
            return data[0]
        return None

    async def get_by_id(self, type_: Type[_Ps2ObjectT], id_: int
                        ) -> Optional[_Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Like :meth:`Client.get()`, but checks the local cache before
        performing the query.

        Arguments:
            type_: The object type to search for.
            id_: The unique ID of the object.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        filters: CensusData = {type_.id_field: id_}
        data = await self.find(type_, results=1, **filters)
        if data and not isinstance(data[0], type_):
            raise RuntimeError(
                f'Expected {type_} instance, got {type(data[0])} instead, '
                'please report this bug to the project maintainers')
        if data:
            return data[0]
        hook: Callable[[int], CensusData]
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
                          locale: str = 'en') -> Optional[_NamedT]:
        """Retrieve an object by its unique name.

        Depending on the ``type_`` specified, this may retrieve a
        cached object, rather than querying the API.

        Keep in mind that not all :class:`Named` objects have a
        localised name; the ``locale`` argument has no effect in these
        cases.

        This query is always case-insensitive.

        Arguments:
            type_: The object type to search for.
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to ``'en'``.

        Returns:
            The entry with the matching name, or ``None`` if not found.

        """
        key = f'{locale}_{name.lower()}'
        _log.debug('%s "%s"[%s] requested', type_.__name__, name, locale)
        # pylint: disable=protected-access
        if (instance := type_._cache.get(key)) is not None:  # type: ignore
            _log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        _log.debug('%s "%s"[%s] not cached, generating API query...',
                   type_.__name__, name, locale)
        query = Query(type_.collection, service_id=self.service_id)
        query.case(False).add_term(field=f'name.{locale}', value=name)
        payload = await self.request(query)
        try:
            payload = extract_single(payload, type_.collection)
        except NotFoundError:
            return None
        return type_(payload, locale=locale, client=self)
