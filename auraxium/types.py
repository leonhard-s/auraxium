"""Custom types used by the auraxium module."""

from typing import Dict, List, Optional, Union

import pydantic

from ._support import deprecated

__all__ = [
    'CensusData',
    'LocaleData'
]

CensusData = Dict[
    str, Union[str, int, float, 'CensusData', List['CensusData']]]


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

    @deprecated('0.3.0', '.name (without parentheses)')
    def __call__(self, locale: str = 'en') -> str:
        return getattr(self, locale)

    def __str__(self) -> str:
        return self.en or repr(self)

    @classmethod
    def empty(cls) -> 'LocaleData':
        """Return an empty :class:`LocaleData` instance.

        This is mostly provided to easily handle payloads who's entire
        localised string field is ``NULL``.
        """
        return cls()
