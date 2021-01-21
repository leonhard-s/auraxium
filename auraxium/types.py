"""Custom types used by the auraxium module."""

from typing import Any, Dict, Optional

import pydantic

__all__ = [
    'CensusData',
    'LocaleData'
]


# NOTE: The inner dict's value is typed as "Any" due to Mypy not supporting
# cycling definitions yet.
CensusData = Dict[str, Any]


class LocaleData(pydantic.BaseModel):
    """Container for localised strings.

    Note that the ``tr`` locale is ignored as it was abandoned by the
    developers and is generally either missing or unpopulated.
    """
    # pylint: disable=too-few-public-methods

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
