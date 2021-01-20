"""Data classes for :mod:`auraxium.ps2.objective`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'ObjectiveData',
    'ObjectiveTypeData'
]

# pylint: disable=too-few-public-methods


class ObjectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Objective`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_id: int
    objective_type_id: int
    objective_group_id: int
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None
    param7: Optional[str] = None
    param8: Optional[str] = None
    param9: Optional[str] = None


class ObjectiveTypeData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.ObjectiveType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_type_id: int
    description: str
    param1: Optional[str] = None
    param2: Optional[str] = None
    param3: Optional[str] = None
    param4: Optional[str] = None
    param5: Optional[str] = None
    param6: Optional[str] = None
    param7: Optional[str] = None
    param8: Optional[str] = None
    param9: Optional[str] = None
