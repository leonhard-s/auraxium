"""Data classes for :mod:`auraxium.ps2.experience`."""

from .base import RESTPayload
from ..types import LocaleData

__all__ = [
    'ExperienceData',
    'ExperienceRankData'
]

# pylint: disable=too-few-public-methods


class ExperienceData(RESTPayload):
    """Data class for :class:`auraxium.ps2.experience.Experience`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    experience_id: int
    description: str
    xp: int


class ExperienceRankData(RESTPayload):
    """Data class for :class:`auraxium.ps2.experience.Experience`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    class EmpireData(RESTPayload):
        """Object representation of an empire-specific sub-key.

        Attributes:
            title: The localised title for this experience rank.
            image_set_id: The image set associated with this rank.
            image_id: The default image asset for this rank.

        """

        title: LocaleData
        image_set_id: int
        image_id: int

    rank: int
    xp_max: int
    vs: EmpireData
    vs_image_path: str
    nc: EmpireData
    nc_image_path: str
    tr: EmpireData
    tr_image_path: str
