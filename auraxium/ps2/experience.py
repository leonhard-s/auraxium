"""Experience and rank class definitions."""

import logging

from ..base import Cached
from ..client import Client
from ..errors import BadPayloadError
from ..models import ExperienceData, ExperienceRankData
from ..types import CensusData

log = logging.getLogger('auraxium.ps2')


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """A type of experience tick."""

    collection = 'experience'
    data: ExperienceData
    id_field = 'experience_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> ExperienceData:
        return ExperienceData.from_census(data)


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
