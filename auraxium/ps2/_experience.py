"""Experience and rank class definitions."""

import logging
from typing import List, Union

import pydantic

from ..base import Cached
from ..errors import PayloadError
from ..models import ExperienceData, ExperienceRankData
from .._rest import RequestClient
from ..types import CensusData

from ._faction import Faction

__all__ = [
    'Experience',
    'ExperienceRank'
]

log = logging.getLogger('auraxium.ps2')


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """A type of experience tick.

    .. attribute:: id
       :type: int

       The unique ID of this experience tick.

    .. attribute:: description
       :type: str

       A description of when this experience reward is
            granted.

    .. attribute:: xp
       :type: int

       The amount of experience points awarded.
    """

    collection = 'experience'
    data: ExperienceData
    id_field = 'experience_id'
    _model = ExperienceData

    # Type hints for data class fallback attributes
    id: int
    description: str
    xp: int


class ExperienceRank:
    """A type of experience tick.

    .. attribute:: rank
       :type: int

       The battle rank value represented by this rank name.

    .. attribute:: xp_max
       :type: int

       (Not yet documented)

    .. attribute:: vs
       :type: auraxium.models.ExperienceRankData.EmpireData

       Empire-specific rank data for VS.

    .. attribute:: vs_image_path
       :type: str

       The VS-specific default image path.

    .. attribute:: nc
       :type: auraxium.models.ExperienceRankData.EmpireData

       Empire-specific rank data for NC.

    .. attribute:: nc_image_path
       :type: str

       The NC-specific default image path.

    .. attribute:: tr
       :type: auraxium.models.ExperienceRankData.EmpireData

       Empire-specific rank data for TR.

    .. attribute:: tr_image_path
       :type: str

       The TR-specific default image path.
    """

    collection = 'experience_rank'
    data: ExperienceRankData
    _model = ExperienceRankData

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
        rank = int(str(data['rank']))
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

        This will take the form of ``<Class:rank:type>``, e.g.
        ``<ExperienceRank:50:ASP>``.
        """
        mode = 'ASP' if self.data.nc.image_id == 88685 else 'Default'
        return f'<{self.__class__.__name__}:{self.data.rank}:{mode}>'
