"""Data classes for :mod:`auraxium.ps2._objective`."""

from .base import RESTPayload

__all__ = [
    'ObjectiveData',
    'ObjectiveTypeData'
]


class ObjectiveData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Objective`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_id: int
    objective_type_id: int
    objective_group_id: int
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
    param6: str | None = None
    param7: str | None = None
    param8: str | None = None
    param9: str | None = None


class ObjectiveTypeData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ObjectiveType`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    objective_type_id: int
    description: str
    param1: str | None = None
    param2: str | None = None
    param3: str | None = None
    param4: str | None = None
    param5: str | None = None
    param6: str | None = None
    param7: str | None = None
    param8: str | None = None
    param9: str | None = None
