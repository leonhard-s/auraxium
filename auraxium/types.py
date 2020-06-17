"""Custom types used by the auraxium module."""

from typing import Any, Callable, Dict, NamedTuple

__all__ = ['CensusData']

# NOTE: This is types as "Any" due to Mypy not supporting cycling definitions
# yet.
CensusData = Dict[str, Any]
