"""Experience and rank class definitions."""

import logging
from typing import List, Union, cast

import pydantic

from ..base import Cached
from ..errors import PayloadError
from ..models import ExperienceData, ExperienceRankData
from .._rest import RequestClient
from ..types import CensusData

from .faction import Faction

__all__ = [
    'Experience',
    'ExperienceRank'
]

log = logging.getLogger('auraxium.ps2')


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """A type of experience tick.

    Attributes:
        experience_id: The unique ID of this experience tick.
        description: A description of when this experience reward is
            granted.
        xp: The amount of experience points awarded.

    """

    collection = 'experience'
    data: ExperienceData
    dataclass = ExperienceData
    id_field = 'experience_id'

    # Type hints for data class fallback attributes
    experience_id: int
    description: str
    xp: int


class ExperienceRank:
    """A type of experience tick.

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

    collection = 'experience_rank'
    data: ExperienceRankData
    dataclass = ExperienceRankData

    # Type hints for data class fallback attributes
    rank: int
    xp_max: int
    vs: ExperienceRankData.EmpireData
    vs_image_path: str
    nc: ExperienceRankData.EmpireData
    nc_image_path: str
    tr: ExperienceRankData.EmpireData
    tr_image_path: str

    def __init__(self, data: CensusData, client: RequestClient) -> None:
        """Initialise the object.

        This populates the object using the provided payload.
        """
        rank = int(cast(str, data['rank']))
        log.debug('Instantiating <%s:%d> using payload: %s',
                  self.__class__.__name__, rank, data)
        self._client = client
        try:
            self.data = ExperienceRankData(**data)
        except pydantic.ValidationError as err:
            raise PayloadError(
                f'Unable to populate {self.__class__.__name__} due to a '
                f'missing key: {err.args[0]}', data) from err

    def image(self, faction: Union[int, Faction]) -> str:
        """Return the default image for this type."""
        if isinstance(faction, Faction):
            faction = faction.id
        internal_tag: List[str] = ['null', 'vs', 'nc', 'tr', 'nso']
        image_id = getattr(self.data, internal_tag[faction])
        url = 'https://census.daybreakgames.com/files/ps2/images/static/'
        return url + f'{image_id}.png'

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of <Class:rank:type>, e.g.
        <ExperienceRank:50:ASP>.

        Returns:
            A string representing the object.

        """
        mode = 'ASP' if self.data.nc.image_id == 88685 else 'Default'
        return f'<{self.__class__.__name__}:{self.data.rank}:{mode}>'
