"""Experience and rank class definitions."""

import logging
from typing import Any, List, Union, cast

import pydantic

from ..base import Cached
from ..endpoints import DBG_FILES
from ..errors import PayloadError
from ..models import (ExperienceAwardTypeData, ExperienceData,
                      ExperienceRankData)
from .._rest import RequestClient
from ..types import CensusData

from ._faction import Faction

__all__ = [
    'Experience',
    'ExperienceAwardType',
    'ExperienceRank'
]

log = logging.getLogger('auraxium.ps2')


class Experience(Cached, cache_size=100, cache_ttu=3600.0):
    """An experience type that can be earned by a character.

    .. note::

       Not all experience types returned through the WebSocket event
       stream's :class:`~auraxium.event.GainExperience` event are
       present in this table.

    .. attribute:: id
       :type: int

       The unique ID of this experience tick. In the API payload, this
       field is called ``experience_id``.

    .. attribute:: description
       :type: str

       A description of when this experience reward is granted.

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


class ExperienceAwardType(Cached, cache_size=100, cache_ttu=3600.0):
    """A collection of related experience types.
    
    .. attribute:: id
       :type: int
       
       The unique ID of this experience award type. In the API payload,
       this field is called ``experience_award_type_id``.

    .. attribute:: name
       :type: str

       Internal name of this experience award type. Not localised or
       designed to be user-facing.
    """

    collection = 'experience_award_type'
    data: ExperienceAwardTypeData
    id_field = 'experience_award_type_id'
    _model = ExperienceAwardTypeData

    # Type hints for data class fallback attributes
    id: int
    name: str


class ExperienceRank:
    """A type of experience tick.

    .. attribute:: rank
       :type: int

       The battle rank value represented by this rank name.

    .. attribute:: xp_max
       :type: int

       The amount of experience needed to achieve this rank.

       .. note::

          Due to the BR 100 / BR 120 level caps, this may not correlate
          estimate the rank of a given character as they might have
          "lost" part of their experience to a level cap in the past.

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
            self.data = ExperienceRankData(**cast(Any, data))
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
        return str(DBG_FILES / f'{image_id}.png')

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of ``<Class:rank:type>``, e.g.
        ``<ExperienceRank:50:ASP>``.
        """
        mode = 'ASP' if self.data.nc.image_id == 88685 else 'Default'
        return f'<{self.__class__.__name__}:{self.data.rank}:{mode}>'
