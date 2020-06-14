"""Custom types used by the auraxium module."""

from typing import Any, Callable, Dict, NamedTuple

__all__ = ['CensusData']

# NOTE: This is types as "Any" due to Mypy not supporting cycling definitions
# yet.
CensusData = Dict[str, Any]


class CensusInfo(NamedTuple):
    """Define relations between Python attributes and API fields.

    The "fields" attribute translates between the Python names and the
    API collection's fields, the "converter" attribute allows for
    custom converter functions between Python types and API values.

    This is useful for converting datetime objects to unix seconds, or
    seconds to milliseconds.

    Attributes:
        fields: A dictionary mapping API names to census names.
        converter: A dictionary mapping API names to the function used
            for conversion. The function will be called when the name
            it is defined under is converted.
    """

    fields: Dict[str, str]
    converter: Dict[str, Callable[[Any], Any]] = {}
