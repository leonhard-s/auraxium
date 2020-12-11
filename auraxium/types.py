"""Custom types used by the auraxium module."""

from typing import Any, Callable, Dict, Optional, TypeVar

import pydantic

__all__ = [
    'CensusData',
    'LocaleData',
    'optional'
]

T = TypeVar('T')  # pylint: disable=invalid-name


# NOTE: The inner dict's value is typed as "Any" due to Mypy not supporting
# cycling definitions yet.
CensusData = Dict[str, Any]


# pylint: disable=no-member
class LocaleData(pydantic.BaseModel):
    """Container for localised strings.

    Note that the ``tr`` locale is ignored as it was abandoned by the
    developers and is generally either missing or unpopulated.
    """

    class Config:
        """Pydantic model configuration.

        This inner class is used to namespace the pydantic
        configuration options.
        """
        allow_mutation = False

    de: Optional[str] = None
    en: Optional[str] = None
    es: Optional[str] = None
    fr: Optional[str] = None
    it: Optional[str] = None

    @classmethod
    def empty(cls) -> 'LocaleData':
        """Return an empty :class:`LocaleData` instance.

        This is mostly provided to easily handle payloads who's entire
        localised string field is ``NULL``.
        """
        return cls()


def optional(data: CensusData, key: str,
             cast: Callable[[Any], T]) -> Optional[T]:
    """Cast an optional dictionary value to a given type.

    This is a helper method that acts much like :meth:`dict.get()`, but
    also casts the retrieved value to the given type if it is not None.

    Arguments:
        data: The dictionary to process.
        key: The key to access.
        cast: The type to cast the value to if it exists.

    Returns:
        The cast value retrieved from the dictionary, or None.

    """
    raw: Optional[T]
    if (raw := data.pop(key, None)) is not None:
        if raw == 'NULL':
            raw = None
        else:
            raw = cast(raw)
    return raw
