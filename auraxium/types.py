"""Custom types used by the auraxium module."""

from typing import Any, Dict

__all__ = [
    'CensusData'
]

# NOTE: The inner dict's value is typed as "Any" due to Mypy not supporting
# cycling definitions yet.
CensusData = Dict[str, Any]
