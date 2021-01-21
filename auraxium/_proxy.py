"""Define the proxy object system."""

import asyncio
import datetime
import warnings
from typing import (Any, Dict, Generator, Generic, Iterator, List, Optional,
                    Type, TypeVar)

from ._base import Ps2Object
from .census import JoinedQuery, Query
from ._client import Client
from ._request import extract_payload

__all__ = [
    'InstanceProxy',
    'Proxy',
    'SequenceProxy'
]

_Ps2ObjectT = TypeVar('_Ps2ObjectT', bound=Ps2Object)


class Proxy(Generic[_Ps2ObjectT]):
    """Base class for any proxy objects.

    The query object passed must specify the parent field name for all
    of its joins. This is necessary to allow parsing of the payload.

    Additionally, this currently does not support custom insertion
    fields.

    Attributes:
        query: The API query used to populate the proxy object.

    """

    def __init__(self, type_: Type[_Ps2ObjectT], query: Query,
                 client: Client, lifetime: float = 60.0) -> None:
        """Initialise the proxy.

        Note that the lifetime argument may not exceed the UTC epoch
        seconds due to the way this value is initialised.

        Arguments:
            type_: The object type represented by the proxy.
            query: The query used to retrieve the data.
            client: The client through which to query the API.
            lifetime (optional): The time-to-use of the retrieved data.
                Defaults to ``60.0``.

        """
        self._type = type_
        self.query = query
        self._client = client
        self._ttu = lifetime
        self._data: List[_Ps2ObjectT]
        self._index: int
        self._lock = asyncio.Lock()
        self._last_fetched = datetime.datetime.utcfromtimestamp(0)
        max_age = datetime.datetime.now() - self._last_fetched
        assert self._ttu < max_age.total_seconds()

    async def _poll(self) -> None:
        """Query the API, retrieving the data.

        This method uses a lock to ensure it does not try to query the
        same object multiple times.

        """
        async with self._lock:
            payload = await self._client.request(self.query)
            list_ = self._resolve_nested_payload(payload)
            # NOTE: There does not appear to be an easy way to type something
            # as "subclass of an abstract class and all abstract methods have
            # been overwritten", which is why this is typed as being a
            # Ps2Object subclass and then promptly ignored here.
            self._data = [self._type(  # type: ignore
                data, client=self._client) for data in list_]
            self._last_fetched = datetime.datetime.now()

    def _resolve_nested_payload(self, payload: Dict[str, Any]
                                ) -> List[Dict[str, Any]]:
        """Resolve the object payload.

        This introspects the given query to determine the sub-key for
        the actual object to return.

        Arguments:
            payload: The raw payload returned from the API.

        Raises:
            RuntimeError: Raised if the query has more than one join.
            RuntimeError: Raised if the parent field of a query is not
                given.

        Returns:
            The native list of payloads, ready for instantiation.

        """

        def resolve_join(join: JoinedQuery, parent: List[Dict[str, Any]]
                         ) -> List[Dict[str, Any]]:
            # NOTE: The parent list will always be a list of all items the join
            # has been applied to. The resulting list should be a merged set of
            # the elements therein.
            assert join.data.collection is not None
            if (on_ := join.data.field_on) is None:
                raise RuntimeError('Parent field of None not supported')
            # Filter out the payload sub-dict corresponding to the given join
            data: List[Dict[str, Any]] = []
            for element in parent:
                value = element[f'{on_}_join_{join.data.collection}']
                if join.data.is_list:
                    data.extend(value)
                else:
                    data.append(value)
            # Recursively resolve any inner joins
            if join.joins:
                parent = data
                data = []
                for inner in join.joins:
                    data.extend(resolve_join(inner, parent))
            return data

        # Main query
        assert self.query.data.collection is not None
        data = extract_payload(payload, self.query.data.collection)
        # Resolve any joins
        if self.query.joins:
            parent = data
            # If any joins were defined, resolve each of the joins and merge
            # their outputs before returning
            data = []
            for join in self.query.joins:
                data.extend(resolve_join(join, parent))
        return data


class SequenceProxy(Proxy[_Ps2ObjectT]):
    """Proxy for lists of results.

    Use this is your joins are returning a list of objects.

    """

    def __aiter__(self) -> 'SequenceProxy[_Ps2ObjectT]':
        self._index = -1
        return self

    async def __anext__(self) -> _Ps2ObjectT:
        age = datetime.datetime.now() - self._last_fetched
        if age.total_seconds() > self._ttu:
            if self._index > -1:
                warnings.warn('Data went stale during iteration, polling new')
            await self._poll()
        self._index += 1
        try:
            return self._data[self._index]
        except IndexError as err:
            raise StopAsyncIteration from err

    def __await__(self) -> Iterator[List[_Ps2ObjectT]]:
        return self.flatten().__await__()

    async def flatten(self) -> List[_Ps2ObjectT]:
        """Retrieve all elements in the response as a list.

        Returns:
            A list of instantiated objects.

        """
        return [e async for e in self]


class InstanceProxy(Proxy[_Ps2ObjectT]):
    """Proxy for a single result.

    Use this is your joins are returning a single object.

    """

    def __await__(self) -> Generator[Any, None, Optional[_Ps2ObjectT]]:
        return self.resolve().__await__()

    async def resolve(self) -> Optional[_Ps2ObjectT]:
        """Return the proxy object.

        Returns:
            The object, or None if no match was found.

        """
        age = datetime.datetime.now() - self._last_fetched
        if age.total_seconds() > self._ttu:
            await self._poll()
        try:
            return self._data[0]
        except IndexError:
            return None
