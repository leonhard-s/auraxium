"""Shared custom types and global type aliases."""

import pydantic

from ._support import deprecated

__all__ = [
    'CensusData',
    'LocaleData'
]

CensusData = dict[str, 'str | int | float | CensusData | list[CensusData]']


class LocaleData(pydantic.BaseModel):
    """Container for localised strings.

    Note that the ``tr`` locale is ignored as it was abandoned by the
    developers and is generally either missing or unpopulated.
    """

    model_config = pydantic.ConfigDict(extra='ignore', frozen=True)

    de: str | None = None
    en: str | None = None
    es: str | None = None
    fr: str | None = None
    it: str | None = None

    @deprecated('0.3', '0.5', ':attr:`auraxium.types.LocaleData.name`')
    def __call__(self, locale: str = 'en') -> str:  # pragma: no cover
        return str(getattr(self, locale))

    def __str__(self) -> str:
        return self.en or repr(self)

    @classmethod
    def empty(cls) -> 'LocaleData':
        """Return an empty :class:`LocaleData` instance.

        This is mostly provided to easily handle payloads who's entire
        localised string field is NULL.
        """
        return cls()
