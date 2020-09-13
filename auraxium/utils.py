"""Shared utility methods used throughout Auraxium."""

from typing import Any, Callable, Dict, NamedTuple, Optional, TypeVar

from .types import CensusData

AnyT = TypeVar('AnyT')


class LocaleData(NamedTuple):
    """Container for localised strings.

    Note that the ``tr`` locale is ignored as it was abandoned by the
    developers and is generally either missing or unpopulated.
    """

    de: str
    en: str
    es: str
    fr: str
    it: str

    @classmethod
    def empty(cls) -> 'LocaleData':
        """Return an empty :class:`LocaleData` instance.

        This is mostly provided to easily handle payloads who's entire
        localised string field is ``NULL``.
        """
        return cls(*(None,)*5)  # type: ignore

    @classmethod
    def from_census(cls, data: CensusData) -> 'LocaleData':
        """Create and populate an instance using the given payload.

        This expects to be passed the inner dictionary containing the
        localisation keys (i.e. ``{'de': '...', 'en': '...', ... }``).
        """
        de_ = optional(data, 'de', str) or 'Missing String'
        en_ = optional(data, 'en', str) or 'Missing String'
        es_ = optional(data, 'es', str) or 'Missing String'
        fr_ = optional(data, 'fr', str) or 'Missing String'
        it_ = optional(data, 'it', str) or 'Missing String'
        # The TR locale is unfinished and deliberately discarded if found
        _ = optional(data, 'tr', str)
        return cls(
            de_,
            en_,
            es_,
            fr_,
            it_)


# NOTE: The functions below are a dummy implementation for testing and will be
# revisited soon.


def nested_dict_get(dict_: Dict[str, Any], key: str) -> Any:
    """Nested dict key access."""
    nested_keys = key.split('.')
    while nested_keys:
        dict_ = dict_[nested_keys.pop(0)]
    return dict_


def nested_dict_pop(dict_: Dict[str, Any], key: str) -> Any:
    """Nested dict access and removal."""

    def nested_pop(sub_: Dict[str, Any], inner: str, *args: str) -> Any:
        if not args:
            return sub_.pop(inner)
        value = nested_pop(sub_[inner], *args)
        if not sub_[inner]:
            del sub_[inner]
        return value

    outer, *inner = key.split('.')
    if not inner:
        return dict_.pop(outer)
    value = nested_pop(dict_[outer], *inner)
    if not dict_[outer]:
        del dict_[outer]
    return value


def optional(data: CensusData, key: str,
             cast: Callable[[Any], AnyT]) -> Optional[AnyT]:
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
    raw: Optional[AnyT]
    if (raw := data.pop(key, None)) is not None:
        if raw == 'NULL':
            raw = None
        else:
            raw = cast(raw)
    return raw
