"""Data classes for :mod:`auraxium.ps2._character`."""

from typing import Optional

from .base import RESTPayload
from ..types import LocaleData
from .._support import deprecated

__all__ = [
    'CharacterAchievement',
    'CharacterData',
    'CharacterDirective',
    'TitleData'
]

# pylint: disable=too-few-public-methods


class CharacterAchievement(RESTPayload):
    """Data container for a character's achievement status.

    .. attribute:: character_id
       :type: int

       The ID of the character for this entry.

    .. attribute:: achievement_id
       :type: int

       The ID of the achievement for this entry.

    .. attribute:: earned_count:
       :type: int

       How often the character has earned the given achievement.

    .. attribute:: start
       :type: int

       The UTC timestamp the character started progression towards this
       achievement at.

       For repeatable achievements, this marks the last time the
       achievement was gained.

    .. attribute:: start_date
       :type: str

       Human-readable version of :attr:`start`.

    .. attribute:: finish
       :type: int

       The time the character completed this achievement. Only valid
       for one-time achievements such as medals.

       For repeatable achievements, this is always 0.

    .. attribute:: finish_date
       :type: str

       Human-readable version of :attr:`finish`.

    .. attribute:: last_save
       :type: int

       The last time the character gained this achievement at as a UTC
       timestamp.

    .. attribute:: last_save_date
       :type: str

       Human-readable version of :attr:`last_save`.
    """

    character_id: int
    achievement_id: int
    earned_count: int
    start: int
    start_date: str
    finish: int
    finish_date: str
    last_save: int
    last_save_date: str


class CharacterData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Character`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    class BattleRank(RESTPayload):
        """Object representation of the "battle_rank" sub-key.

        .. attribute:: value
           :type: int

           The current battle rank of the character.

        .. attribute:: percent_to_next
           :type: float

           The progress to the next battle rank.
        """

        value: int
        percent_to_next: float

    class Certs(RESTPayload):
        """Object representation of the "certs" sub-key.

        .. attribute:: earned_points
           :type: int

           Certification points the player has ever earned.

        .. attribute:: gifted_points
           :type: int

           Certification points the player was gifted through events.

        .. attribute:: spent_points
           :type: int

           Certification points the character has spent.

        .. attribute:: available_points
           :type: int

           The current certification point balance of the character.

        .. attribute:: percent_to_next
            :type: float

            The progress to the next certification point for the
            character.
            """

        earned_points: int
        gifted_points: int
        spent_points: int
        available_points: int
        percent_to_next: float

    class DailyRibbon(RESTPayload):
        """Object representation of the "daily_ribbon" sub-key.

        .. note::

           As of spring 2021, daily ribbon boni are disabled and
           unused.

        .. attribute:: count
           :type: int

           The number of daily ribbon boni available.

        .. attribute:: time
           :type: int

           The time the next daily ribbon bonus will be granted.

        .. attribute:: date
            type: str

            Human-readable version of :attr:`time`.
        """

        count: int  # type: ignore
        time: Optional[int] = None
        date: Optional[str] = None

    class Name(RESTPayload):
        """Object representation of the "name" sub-key.

        .. note::

           This object supports casting this object to :class:`str`,
           which will return the name of the player.

        .. attribute:: first
           :type: str

           Unique name of the player.

        .. attribute:: first_lower
           :type: str

           Lowercase version of :attr:`first`. Useful for
           case-insensitive name lookups without requiring the use of
           a case-insensitive query.
        """

        first: str
        first_lower: str

        @deprecated('0.2', '0.3', replacement=':attr:`auraxium.models.'
                    'CharacterData.Name.name`')
        def __call__(self, locale: str = 'en') -> str:  # pragma: no cover
            return self.first

        def __str__(self) -> str:
            return self.first

    class Times(RESTPayload):
        """Object representation of the "times" sub-key.

        .. attribute:: creation
           :type: int

           The time the character was created.

        .. attribute:: creation_date
           :type: str

           Human-readable version of :attr:`creation`.

        .. attribute:: last_save
           :type: int

           The last time the character was updated. This roughly
           matches the last time the character logged out.

        .. attribute:: last_save_date
           :type: str

           Human-readable version of :attr:`last_save`.

        .. attribute:: last_login
           :type: int

           The last time the character logged in.

        .. attribute:: last_login_date
           :type: str

           Human-readable version of :attr:`last_login_date`.

        .. attribute:: login_count
           :type: int

           The number of times the character has logged in.

        .. attribute:: minutes_played
           :type: int

           The total number of minutes this character was logged in.
        """

        creation: int
        creation_date: str
        last_save: int
        last_save_date: str
        last_login: int
        last_login_date: str
        login_count: int
        minutes_played: int

    character_id: int
    name: Name
    faction_id: int
    head_id: int
    title_id: int
    times: Times
    certs: Certs
    battle_rank: BattleRank
    profile_id: int
    daily_ribbon: DailyRibbon
    prestige_level: int


class CharacterDirective(RESTPayload):
    """Data container for a character's directive status.

    .. attribute:: character_id
       :type: int

       The ID of the character for this entry.

    .. attribute: directive_id
       :type: int

       The ID of the directive for this entry.


    .. attribute:: directive_tree_id
       :type: int

       The ID of the directive tree for this entry.

    .. attribute:: completion_time
       :type: int

       The time the character completed this directive.

    .. attribute:: completion_time_date
       :type: str

       Human-readable version of :attr:`completion_time`.
    """

    character_id: int
    directive_tree_id: int
    directive_id: int
    completion_time: int
    completion_time_date: str


class CharacterDirectiveObjective(RESTPayload):
    """Data container for a characters's directive progress.

    .. attribute:: character_id
       :type: int

       The ID of the character for this entry.
    .. attribute:: directive_id
       :type: int

       The ID of the directive for this entry.

    .. attribute:: objective_id
       :type: int

       ID of the objective.

    .. attribute:: objective_group_id
       :type: int

       (More info needed)

    .. attribute:: status
       :type: int

       The status of this objective.

    .. attribute:: state_data
       :type: int

       Extra data for this state.
    """

    character_id: int
    directive_id: int
    objective_id: int
    objective_group_id: int
    status: int
    state_data: int


class CharacterDirectiveTier(RESTPayload):
    """Data container for character directive tier progress.

    .. attribute:: character_id
       :type: int

       ID of the character.

    .. attribute:: directive_tree_id
       :type: int

       ID of the directive tree.

    .. attribute:: directive_tier_id
       :type: int

       ID of the directive tier.

    .. attribute:: completion_time
       :type: int

       When this tier was completed, or zero if not yet completed.

    .. attribute:: completion_time_date
       :type: int

       String version of :attr:`completion_time`.
    """

    character_id: int
    directive_tree_id: int
    directive_tier_id: int
    completion_time: int
    completion_time_date: str


class CharacterDirectiveTree(RESTPayload):
    """Data container for character directive tree progress.

    .. attribute:: character_id
       :type: int

       ID of the character.

    .. attribute:: directive_tree_id
       :type: int

       The directive tree for this entry.

    .. attribute:: current_directive_tier_id
       :type: int

       The current tier the character is on for the given directive
       tree.

    .. attribute:: current_level
       :type: int

       The current level in this directive tree.

    .. attribute:: completion_time
       :type: int

       When the directive tree was compled, or zero if not yet
       completed.

    .. attribute:: completion_time_date
       :type: int

       String version of :attr:`completion_time`.
    """

    character_id: int
    directive_tree_id: int
    current_directive_tier_id: int
    current_level: int
    completion_time: int
    completion_time_date: str


class TitleData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Title`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    title_id: int
    name: LocaleData
