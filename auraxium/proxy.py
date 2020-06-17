"""Define the proxy object system."""

import asyncio
import datetime
import warnings
from typing import Any, Dict, Generic, Iterator, List, Optional, Type, TypeVar

from .base import Ps2Object
from .census import Query
from .client import Client
from .request import extract_payload, run_query

Ps2ObjectT = TypeVar('Ps2ObjectT', bound=Ps2Object)


class Proxy(Generic[Ps2ObjectT]):
    """Base class for any proxy objects.

    The query object passed must specify the parent field name for all
    of its joins. This is necessary to allow parsing of the payload.

    Additionally, this currently does not support custom insertion
    fields.

    Attributes:
        query: The API query used to populate the proxy object.

    """

    def __init__(self, type_: Type[Ps2ObjectT], query: Query,
                 client: Client, lifetime: float = 60.0) -> None:
        """Initialise the proxy.

        Note that the lifetime argument may not exceed the UTC epoch
        seconds due to the way this value is initialised.

        Args:
            type_: The object type represented by the proxy
            query: The query used to retrieve the data
            client: The client through which to query the API
            lifetime (optional): The time-to-use of the retrieved data.
                Defaults to 60.0.

        """
        self._type = type_
        self.query = query
        self._client = client
        self._ttu = lifetime

        self._data: List[Ps2ObjectT]
        self._index: int
        self._lock = asyncio.Lock()
        self._last_fetched = datetime.datetime.utcfromtimestamp(0)

        max_age = datetime.datetime.now() - self._last_fetched
        assert self._ttu < max_age.total_seconds()

    async def _poll(self) -> None:
        """Query the API, retrieving the data."""
        async with self._lock:
            payload = await run_query(
                self.query, session=self._client.session)
            list_ = self._resolve_nested_payload(payload)
            self._data = [self._type(data, self._client) for data in list_]
            self._last_fetched = datetime.datetime.now()

    def _resolve_nested_payload(self, payload: Dict[str, Any]
                                ) -> List[Dict[str, Any]]:
        """Resolve the object payload.

        This introspects the given query to determine the sub-key for
        the actual object to return.

        Args:
            payload: The raw payload returned from the API

        Raises:
            RuntimeError: Raised if the query has more than one join
            RuntimeError: Raised if the parent field of a query is not
                given

        Returns:
            The native list of payloads, ready for instantiation

        """
        # Main query
        assert self.query.collection is not None
        outer_list = extract_payload(payload, self.query.collection)
        # Resolve join, this may be the final type or an intermediate type
        if self.query.joins:
            join = self.query.joins[0]
            assert join.collection is not None
            if len(self.query.joins) > 1:
                raise RuntimeError('Proxy only supports one joined query')
            on_ = join.parent_field
            if on_ is None:
                raise RuntimeError('Parent field of None not supported')
            joins_list = [
                i[f'{on_}_join_{join.collection}'] for i in outer_list]
            if join.joins:
                inner = join.joins[0]
                assert inner.collection is not None
                if len(join.joins) > 1:
                    raise RuntimeError('Proxy only supports one nested join')
                on_ = inner.parent_field
                if on_ is None:
                    raise RuntimeError('Parent field of None not supported')
                joins_list = [
                    i[f'{on_}_join_{inner.collection}'] for i in joins_list[0]]
            return joins_list
        return outer_list


class SequenceProxy(Proxy[Ps2ObjectT]):
    """Proxy for lists of results.

    Use this is your joins are returning a list of objects.

    """

    def __aiter__(self) -> 'SequenceProxy[Ps2ObjectT]':
        self._index = -1
        return self

    async def __anext__(self) -> Ps2ObjectT:
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

    def __await__(self) -> Iterator[List[Ps2ObjectT]]:
        return self.flatten().__await__()

    async def flatten(self) -> List[Ps2ObjectT]:
        """Retrieve all elements in the response as a list.

        Returns:
            A list of instantiated objects.

        """
        return [e async for e in self]


class InstanceProxy(Proxy[Ps2ObjectT]):
    """Proxy for lists of results.

    Use this is your joins are returning a single object.

    """

    def __await__(self) -> Iterator[Optional[Ps2ObjectT]]:
        return self.resolve().__await__()

    async def resolve(self) -> Optional[Ps2ObjectT]:
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
