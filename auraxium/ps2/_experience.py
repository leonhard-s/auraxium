"""Experience and rank class definitions."""

import logging
from typing import Any, cast

import pydantic

from ..base import Cached
from ..census import Query
from ..endpoints import DBG_FILES
from ..errors import PayloadError
from ..collections import (ExperienceAwardTypeData, ExperienceData,
                           ExperienceRankData, ExperienceRankFactionData)
from .._proxy import InstanceProxy
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

    .. attribute:: experience_award_type_id
       :type: int | None

       The ID of the :class:`ExperienceAwardType` this experience type
       belongs to. Not set for all experience types.

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
    experience_award_type_id: int | None

    def experience_award_type(self) -> InstanceProxy['ExperienceAwardType']:
        """Return the faction that has access to this item.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        value = self.data.experience_award_type_id or -1
        query = Query(ExperienceAwardType.collection, self._client.service_id)
        query.add_term(field=ExperienceAwardType.id_field, value=value)
        return InstanceProxy(ExperienceAwardType, query, client=self._client)


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
       :type: auraxium.collections.experience_rank.ExperienceRankFaction

       Empire-specific rank data for VS.

    .. attribute:: vs_image_path
       :type: str

       The VS-specific default image path.

    .. attribute:: nc
       :type: auraxium.collections.experience_rank.ExperienceRankFaction

       Empire-specific rank data for NC.

    .. attribute:: nc_image_path
       :type: str

       The NC-specific default image path.

    .. attribute:: tr
       :type: auraxium.collections.experience_rank.ExperienceRankFaction

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
    vs: ExperienceRankFactionData
    vs_image_path: str
    nc: ExperienceRankFactionData
    nc_image_path: str
    tr: ExperienceRankFactionData
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

    def image(self, faction: int | Faction) -> str:
        """Return the default image for this type."""
        if isinstance(faction, Faction):
            faction = faction.id
        if faction <= 0 or faction >= 4:
            raise ValueError(f'Invalid faction ID: {faction}, only 1-3 allowed.')
        internal_tag: list[str] = ['null', 'vs', 'nc', 'tr']
        image_id = getattr(self.data, internal_tag[faction]).image_id
        return str(DBG_FILES / f'{image_id}.png')

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of ``<Class:rank:type>``, e.g.
        ``<ExperienceRank:50:ASP>``.
        """
        # NOTE: Titles are messed up; A.S.P. (i.e. prestige) just copy-pasted
        # all ranks and changed the image, and NSO is not modelled at all.
        # This is a best-effort to at least tell A.S.P. and regular ranks
        # apart for the non-robot factions.
        if '94469' in (self.data.vs_image_path or ''):
            mode = 'ASP'
        else:
            mode = 'Default'
        return f'<{self.__class__.__name__}:{self.data.rank}:{mode}>'
