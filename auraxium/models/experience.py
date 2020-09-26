"""Data classes for :mod:`auraxium.ps2.experience`."""

import dataclasses

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData

__all__ = [
    'ExperienceData',
    'ExperienceRankData'
]


@dataclasses.dataclass(frozen=True)
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
    xp: int  # pylint: disable=invalid-name

    @classmethod
    def from_census(cls, data: CensusData) -> 'ExperienceData':
        return cls(
            int(data.pop('experience_id')),
            str(data.pop('description')),
            int(data.pop('xp')))


@dataclasses.dataclass(frozen=True)
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

    @dataclasses.dataclass(frozen=True)
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

        @classmethod
        def from_census(cls, data: CensusData
                        ) -> 'ExperienceRankData.EmpireData':
            """Populate the data class with values from the dictionary.

            This parses the API response and casts the appropriate
            types.
            """
            return cls(
                LocaleData.from_census(data.pop('title')),
                int(data.pop('image_set_id')),
                int(data.pop('image_id')))

    rank: int
    xp_max: int
    vs: EmpireData  # pylint: disable=invalid-name
    vs_image_path: str
    nc: EmpireData  # pylint: disable=invalid-name
    nc_image_path: str
    tr: EmpireData  # pylint: disable=invalid-name
    tr_image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ExperienceRankData':
        return cls(
            int(data.pop('rank')),
            int(data.pop('xp_max')),
            cls.EmpireData.from_census(data.pop('vs')),
            str(data.pop('vs_image_path')),
            cls.EmpireData.from_census(data.pop('nc')),
            str(data.pop('nc_image_path')),
            cls.EmpireData.from_census(data.pop('tr')),
            str(data.pop('tr_image_path')))
