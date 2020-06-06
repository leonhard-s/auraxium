"""Custom types used by the auraxium module."""

from typing import Any, Callable, Dict, List, NamedTuple

__all__ = ['CensusData']

# NOTE: This is types as "Any" due to Mypy not supporting cycling definitions
# yet.
CensusData = Dict[str, Any]


class CensusInfo(NamedTuple):
    """Used to convert between stuffs."""

    fields: Dict[str, str]
    exclude: List[str] = []
    converter: Dict[str, Callable[[Any], Any]] = {}
