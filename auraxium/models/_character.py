"""Data classes for :mod:`auraxium.ps2.character`."""

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

    Attributes:
        character_id: The ID of the character for this entry.
        achievement_id: The ID of the achievement for this entry.
        earned_count: How often the character has earned the given
            achievement.
        start: The UTC timestamp the character started progression
            towards this achievement at.
        start_date: Human-readable version of :attr:`start`.
        finish: The time the character completed this achievement. Only
            valid for one-time achievements such as medals.
        finish_date: Human-readable version of :attr:`finish`.
        last_save: The last time the character gained this
            achievement at as a UTC timestamp.
        last_save_date: Human-readable version of :attr:`last_save`.

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

        Attributes:
            value: The current battle rank.
            percent_to_next: The progress to the next battle rank.

        """

        value: int
        percent_to_next: float

    class Certs(RESTPayload):
        """Object representation of the "certs" sub-key.

        Attributes:
            earned_points: Certification points the player has ever
                earned.
            gifted_points: Certification points the player was gifted
                through events.
            spent_points: Certification points the character has spent.
            available_points: The current certification point balance
                of the character.
            percent_to_next: The progress to the next certification
                point for the character.

            """

        earned_points: int
        gifted_points: int
        spent_points: int
        available_points: int
        percent_to_next: float

    class DailyRibbon(RESTPayload):
        """Object representation of the "daily_ribbon" sub-key.

        Attributes:
            count: The number of daily ribbon bonuses available.
            time: (Not yet documented)
            date: Human-readable version of :attr:`time`.

        """

        count: int  # type: ignore
        time: Optional[int] = None
        date: Optional[str] = None

    class Name(RESTPayload):
        """Object representation of the "name" sub-key.

        Attributes:
            first: The name of the character.
            first_lower: Lowercase version of :attr:`first`.

        """

        first: str
        first_lower: str

        @deprecated('0.3.0', '.name (without parentheses)')
        def __call__(self, locale: str = 'en') -> str:
            return self.first

        def __str__(self) -> str:
            return self.first

    class Times(RESTPayload):
        """Object representation of the "times" sub-key.

        Attributes:
            creation: The time the character was created.
            creation_date: Human-readable version of :attr:`creation`.
            last_save: The last time the character was updated. This
                roughly matches the last time the character logged out.
            last_save_date: Human-readable version of
                :attr:`last_save`.
            last_login: The last time the character logged in.
            last_login_date: Human-readable version of
                :attr:`last_login_date`.
            login_count: The number of times the character has logged
                in.
            minutes_played: The total number of minutes this character
                was logged into PS2.

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

    Attributes:
        character_id: The ID of the character for this entry.
        directive_tree_id: The ID of the directive tree for this entry.
        directive_id: The ID of the directive for this entry.
        completion_time: The time the character completed this
            directive.
        completion_time_date: Human-readable version of
            :attr:`completion_time`.

    """

    character_id: int
    directive_tree_id: int
    directive_id: int
    completion_time: int
    completion_time_date: str


class TitleData(RESTPayload):
    """Data class for :class:`auraxium.ps2.Title`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    title_id: int
    name: LocaleData
