"""Data classes for :mod:`auraxium.ps2.objective`."""

from typing import Optional

from ..base import Ps2Data

__all__ = [
    'ObjectiveData',
    'ObjectiveTypeData'
]


class ObjectiveData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Objective`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        objective_id: The unique ID of this objective.
        objective_type_id: The associated objective type for this
            objective.
        objective_group_id: The objective group this objective
            contributes to. Used to link objectives to directives.
        param*: Type-specific parameters for this objective. Refer to
            the corresponding :class:`ObjectiveType` for details.

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

    Attributes:
        objective_type_id: The unique ID of the objective type.
        description: A description of what the objective type is used
            for.
        param*: Descriptions of what the corresponding parameter is
            used for in objectives of this type.

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
