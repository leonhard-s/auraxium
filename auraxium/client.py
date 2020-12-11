"""Defines the main client for Auraxium.

This includes both the core methods used to interface with the REST
API, as well as the websocket client used to access the real-time event
streaming service (ESS).

"""

import asyncio
import copy
import logging
from typing import Any, List, Literal, Optional, Type, TYPE_CHECKING, TypeVar, cast
from types import TracebackType

import aiohttp

from .census import Query
from .request import run_query
from .types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. This avoids a circular import at runtime.
    from .base import Named, Ps2Object

__all__ = [
    'Client'
]

ClientT = TypeVar('ClientT', bound='Client')
NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')
log = logging.getLogger('auraxium.client')


class Client:
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

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None,
                 service_id: str = 's:example', profiling: bool = False
                 ) -> None:
        """Initialise a new Auraxium client.

        If loop is not specified, it will be retrieved is using
        :meth:`asyncio.get_event_loop()`.

        Arguments:
            loop (optional): A pre-existing event loop to use for the
                client. Defaults to ``None``.
            service_id (optional): The unique, private service ID of
                the client. Defaults to ``'s:example'``.
            profiling (optional): Whether to enable query and socket
                profiling.

        """
        self.loop = loop or asyncio.get_event_loop()
        self.profiling = profiling
        self._timing_cache: List[float] = []
        self.service_id = service_id
        self.session = aiohttp.ClientSession()

    async def __aenter__(self: ClientT) -> ClientT:
        """Enter the context manager and return the client."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> Literal[False]:
        """Exit the context manager.

        This closes the internal HTTP session before exiting, no error
        handling will be performed.

        Arguments:
            exc_type: The type of exception that was raised.
            exc_value: The exception value that was raised.
            traceback: The traceback type of the exception.

        Returns:
            Always False, i.e. no error suppression.

        """
        await self.close()
        return False  # Do not suppress any exceptions

    @property
    def latency(self) -> float:
        """Return the average request latency for the client.

        This averages up to the last 100 query times. Use the logging
        utility to gain more insight into which queries take the most
        time.

        """
        if not self._timing_cache:
            return -1.0
        return sum(self._timing_cache) / len(self._timing_cache)

    async def close(self) -> None:
        """Shut down the client.

        This will end the HTTP session used for requests to the REST
        API.

        Call this to clean up before the client object is destroyed.

        """
        log.info('Shutting down client')
        await self.session.close()

    async def count(self, type_: Type[Ps2ObjectT], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Arguments:
            type_: The object type to search for.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        return await type_.count(client=self, **kwargs)

    async def find(self, type_: Type[Ps2ObjectT], results: int = 10,
                   offset: int = 0, promote_exact: bool = False,
                   check_case: bool = True, **kwargs: Any) -> List[Ps2ObjectT]:
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
        data = await type_.find(results=results, offset=offset,
                                promote_exact=promote_exact,
                                check_case=check_case,
                                client=self, **kwargs)
        data = cast(List[Ps2ObjectT], data)
        if data and not isinstance(data[0], type(self)):
            raise RuntimeError(
                f'Expected {type(self)} instance, got {type(data[0])} '
                f'instead, please report this bug to the project maintainers')
        return data

    async def get(self, type_: Type[Ps2ObjectT], check_case: bool = True,
                  **kwargs: Any) -> Optional[Ps2ObjectT]:
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
        data = await type_.get(check_case=check_case, client=self, **kwargs)
        data = cast(Optional[Ps2ObjectT], data)
        if data is not None and not isinstance(data, type(self)):
            raise RuntimeError(
                f'Expected {type(self)} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data

    async def get_by_id(self, type_: Type[Ps2ObjectT], id_: int
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Like :meth:`Client.get()`, but checks the local cache before
        performing the query.

        Arguments:
            type_: The object type to search for.
            id_: The unique ID of the object.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        data = await type_.get_by_id(id_, client=self)
        data = cast(Optional[Ps2ObjectT], data)
        if data is not None and not isinstance(data, type(self)):
            raise RuntimeError(
                f'Expected {type(self)} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data

    async def get_by_name(self, type_: Type[NamedT], name: str, *,
                          locale: str = 'en') -> Optional[NamedT]:
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
        data = await type_.get_by_name(name, locale=locale, client=self)
        data = cast(Optional[NamedT], data)
        if data is not None and not isinstance(data, type(self)):
            raise RuntimeError(
                f'Expected {type(self)} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data

    async def request(self, query: Query, verb: str = 'get') -> CensusData:
        """Perform a REST API request.

        This performs the query and performs error checking to ensure
        the query is valid.

        Refer to the :meth:`auraxium.request.raise_for_dict()` method
        for a list of exceptions raised from API errors.

        Arguments:
            query: The query to perform.
            verb (optional): The query verb to utilise.
                Defaults to ``'get'``.

        Returns:
            The API response payload received.

        """
        if self.profiling:
            # Create a copy of the query before modifying it
            query = copy.copy(query)
            query.timing(True)
        data = await run_query(query, verb=verb, session=self.session)
        if self.profiling and verb == 'get':
            timing = data.pop('timing')
            if log.level <= logging.DEBUG:
                url = query.url()
                log.debug('Query times for "%s?%s": %s',
                          '/'.join(url.parts[-2:]), url.query_string,
                          ', '.join([f'{k}: {v}' for k, v in timing.items()]))
            self._timing_cache.append(float(timing['total-ms']))
        return data
