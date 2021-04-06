"""Defines the main client for Auraxium.

This includes both the core methods used to interface with the REST
API, as well as the websocket client used to access the real-time event
streaming service (ESS).

"""

import logging
from typing import Any, List, Optional, Type, TYPE_CHECKING, TypeVar

from ._rest import RequestClient

if TYPE_CHECKING:  # pragma: no cover
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

    async def count(self, type_: Type['Ps2Object'], **kwargs: Any) -> int:
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
        if data and not isinstance(data[0], type_):
            raise RuntimeError(
                f'Expected {type_} instance, got {type(data[0])} '
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
        if data is not None and not isinstance(data, type_):
            raise RuntimeError(
                f'Expected {type_} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data  # type: ignore

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
        if data is not None and not isinstance(data, type_):
            raise RuntimeError(
                f'Expected {type_} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data  # type: ignore

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
        if data is not None and not isinstance(data, type_):
            raise RuntimeError(
                f'Expected {type_} instance, got {type(data)} instead, '
                'please report this bug to the project maintainers')
        return data  # type: ignore
