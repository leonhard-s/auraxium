"""Client object definition."""

import asyncio
from typing import Any, List, Literal, Optional, Type, TYPE_CHECKING, TypeVar
from types import TracebackType

import aiohttp

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the forward
    # references. During runtime, this would cause a circular import.
    from .base import Named, Ps2Object

__all__ = ['Client']

NamedT = TypeVar('NamedT', bound='Named')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')


class Client:
    """The top-level interface for navigating the API."""

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None,
                 service_id: str = 's:example') -> None:
        """Initialise a new ARX client.

        If loop is not specified, it will be retrieved is using
        asyncio.get_event_loop().

        Args:
            loop (optional): A pre-existing event loop to use for the
                client. Defaults to None.
            service_id (optional): The unique, private service ID of
                the client. Defaults to 's:example'.

        """
        self.locale: Optional[str] = None
        self.loop = loop or asyncio.get_event_loop()
        self.retry_queries = True
        self.service_id = service_id
        self.session = aiohttp.ClientSession()
        self.profiling = False

    async def __aenter__(self) -> 'Client':
        """Enter the context manager and return the client."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> Literal[False]:
        """Exit the ontext manager.

        This closes the internal HTTP session before exiting, no error
        handling will be performed.

        Args:
            exc_type: The type of exception that was raised.
            exc_value: The exception value that was raised.
            traceback: The traceback type of the exception.

        Returns:
            Always False, i.e. no error suppression.

        """
        await self.session.close()
        return False  # Do not suppress any exceptions

    async def close(self) -> None:
        """Shut down the client."""
        await self.session.close()

    async def count(self, type_: Type[Ps2ObjectT], **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Args:
            type_: The object type to search for.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        return await type_.count(client=self, **kwargs)

    async def find(self, type_: Type[Ps2ObjectT], results: int = 10,
                   offset: int = 0,
                   promote_exact: bool = False, check_case: bool = True,
                   **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Args:
            type_: The object type to search for.
            results (optional): The maximum number of results. Defaults
                to 10.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to 0.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to False.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

        """
        return await type_.find(results=results, offset=offset,
                                promote_exact=promote_exact,
                                check_case=check_case, client=self, **kwargs)

    async def get(self, type_: Type[Ps2ObjectT], check_case: bool = True,
                  **kwargs: Any) -> Optional[Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like Ps2Object.get(), but will only return one item.

        Args:
            type_: The object type to search for.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
            **kwargs: Any number of filters to apply.

        Returns:
            A matching entry, or None if not found.

        """
        return await type_.get(check_case=check_case, **kwargs)

    async def get_by_id(self, type_: Type[Ps2ObjectT], id_: int
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Args:
            type_: The object type to search for.
            id_: The unique ID of the object.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        return await type_.get_by_id(id_, client=self)

    async def get_by_name(self, type_: Type[NamedT], name: str, *,
                          locale: str = 'en') -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        Args:
            type_: The object type to search for.
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to 'en'.

        Returns:
            The entry with the matching name, or None if not found.

        """
        return await type_.get_by_name(name, locale=locale, client=self)
