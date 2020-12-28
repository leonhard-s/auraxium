"""Data classes for :mod:`auraxium.ps2.experience`."""

from ..base import Ps2Data
from ..types import LocaleData

__all__ = [
    'ExperienceData',
    'ExperienceRankData'
]


class ExperienceData(Ps2Data):
    """Data class for :class:`auraxium.ps2.experience.Experience`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        experience_id: The unique ID of this experience tick.
        description: A description of when this experience reward is
            granted.
        xp: The amount of experience points awarded.

    """

    experience_id: int
    description: str
    xp: int


class ExperienceRankData(Ps2Data):
    """Data class for :class:`auraxium.ps2.experience.Experience`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        rank: The battle rank value represented by this rank name.
        xp_max: (Not yet documented)
        vs: Empire-specific rank data for VS.
        vs_image_path: The VS-specific default image path.
        nc: Empire-specific rank data for NC.
        nc_image_path: The NC-specific default image path.
        tr: Empire-specific rank data for TR.
        tr_image_path: The TR-specific default image path.

    """

    class EmpireData(Ps2Data):
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
