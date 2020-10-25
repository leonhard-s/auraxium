"""Experience and rank class definitions."""

import logging
from typing import List, TYPE_CHECKING, Union

import pydantic

from ..base import Cached
from ..client import Client
from ..errors import PayloadError
from ..models import ExperienceData, ExperienceRankData
from ..types import CensusData

if TYPE_CHECKING:
    from ..ps2 import Faction

log = logging.getLogger('auraxium.ps2')


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """A type of experience tick."""

    collection = 'experience'
    data: ExperienceData
    dataclass = ExperienceData
    id_field = 'experience_id'


class ExperienceRank:
    """A type of experience tick."""

    collection = 'experience_rank'
    data: ExperienceRankData
    dataclass = ExperienceRankData

    def __init__(self, data: CensusData, client: Client) -> None:
        """Initialise the object.

        This populates the object using the provided payload.
        """
        rank = int(data['rank'])
        log.debug('Instantiating <%s:%d> using payload: %s',
                  self.__class__.__name__, rank, data)
        self._client = client
        try:
            self.data = ExperienceRankData(**data)
        except pydantic.ValidationError as err:
            raise PayloadError(
                f'Unable to populate {self.__class__.__name__} due to a '
                f'missing key: {err.args[0]}', data) from err

    def image(self, faction: Union[int, 'Faction']) -> str:
        """Return the default image for this type."""
        from ..ps2 import Faction  # pylint: disable=import-outside-toplevel
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
