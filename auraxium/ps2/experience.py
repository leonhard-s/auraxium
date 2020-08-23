"""Experience and rank class definitions."""

import dataclasses
import logging
from typing import NamedTuple

from ..base import Cached, Ps2Data
from ..client import Client
from ..errors import BadPayloadError
from ..types import CensusData
from ..utils import LocaleData

log = logging.getLogger('auraxium.ps2')


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
    xp: int

    @classmethod
    def from_census(cls, data: CensusData) -> 'ExperienceData':
        return cls(
            int(data['experience_id']),
            str(data['description']),
            int(data['xp']))


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """A type of experience tick."""

    collection = 'experience'
    data: ExperienceData
    id_field = 'experience_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ExperienceData:
        return ExperienceData.from_census(data)


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

    class EmpireData(NamedTuple):
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
            return cls(
                LocaleData.from_census(data['title']),
                int(data['image_set_id']),
                int(data['image_id']))

    rank: int
    xp_max: int
    vs: EmpireData
    vs_image_path: str
    nc: EmpireData
    nc_image_path: str
    tr: EmpireData
    tr_image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ExperienceRankData':
        return cls(
            int(data['rank']),
            int(data['xp_max']),
            cls.EmpireData.from_census(data['vs']),
            str(data['vs_image_path']),
            cls.EmpireData.from_census(data['nc']),
            str(data['nc_image_path']),
            cls.EmpireData.from_census(data['tr']),
            str(data['tr_image_path']))


class ExperienceRank:
    """A type of experience tick."""

    collection = 'experience_rank'
    data: ExperienceRankData

    def __init__(self, data: CensusData, client: Client) -> None:
        """Initialise the object.

        This populates the object using the provided payload.
        """
        rank = int(data['rank'])
        log.debug('Instantiating <%s:%d> using payload: %s',
                  self.__class__.__name__, rank, data)
        self._client = client
        try:
            self.data = ExperienceRankData.from_census(data)
        except KeyError as err:
            raise BadPayloadError(
                f'Unable to populate {self.__class__.__name__} due to a '
                f'missing key: {err.args[0]}') from err

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of <Class:rank:type>, e.g.
        <ExperienceRank:50:ASP>.

        Returns:
            A string representing the object.

        """
        mode = 'ASP' if self.data.nc.image_id == 88685 else 'Default'
        return f'<{self.__class__.__name__}:{self.data.rank}:{mode}>'
