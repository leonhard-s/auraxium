"""Data classes for player statistics payloads."""

from typing import Dict, List

from ..base import Ps2Data


class CharacterStat(Ps2Data):
    """Data class for ``characters_stat`` payloads.

    This is a generic payload that is returned multiple times per
    character. Use the :attr:`stat_name` field to determine the
    statistic returned.

    The :attr:`character_id`, :attr:`profile_id`, and :attr:`stat_name`
    fields create a unique composite key for the table.

    .. note::

        Not every profile has a value for every stat.

    Attributes:
        character_id: The character to which this stat belongs.
        stat_name: The name of the stat returned.
        profile_id: The profile (i.e. class or vehicle) for this stat.
        value_forever: Character-wide, all time value.
        value_monthly: Last 30 days, not calendar months.
        value_weekly: Last 7 days, not calendar weeks.
        value_daily: Last 24 hours, not calendar days.
        value_one_life_max: Highest value ever achieved without dying.
        last_save: The UTC timestamp this value was last updated.
        last_save_date: String version of :attr:`last_save`.

    """

    character_id: int
    stat_name: str
    profile_id: int
    value_forever: float
    value_monthly: float
    value_weekly: float
    value_daily: float
    value_one_life_max: float
    last_save: int
    last_save_date: str


class CharacterStatByFaction(Ps2Data):
    """Data class for ``characters_stat_by_faction`` payloads.

    This is a generic payload that is returned multiple times per
    character. Use the :attr:`stat_name` field to determine the
    statistic returned.

    The :attr:`character_id`, :attr:`profile_id`, and :attr:`stat_name`
    fields create a unique composite key for the table.

    .. note::

        Not every profile has a value for every stat.

    Attributes:
        character_id: The character to which this stat belongs.
        stat_name: The name of the stat returned.
        profile_id: The profile (i.e. class or vehicle) for this stat.
        value_forever_vs: Character-wide, all time value.
        value_forever_nc: See :attr:`value_forever_vs`.
        value_forever_tr: See :attr:`value_forever_vs`.
        value_monthly_vs: Last 30 days, not calendar months.
        value_monthly_nc: See :attr:`value_monthly_vs`.
        value_monthly_tr: See :attr:`value_monthly_vs`.
        value_weekly_vs: Last 7 days, not calendar weeks.
        value_weekly_nc: See :attr:`value_weekly_vs`.
        value_weekly_tr: See :attr:`value_weekly_vs`.
        value_daily_vs: Last 24 hours, not calendar days.
        value_daily_nc: See :attr:`value_daily_vs`.
        value_daily_tr: See :attr:`value_daily_vs`.
        value_one_life_max_vs: Highest value ever achieved without dying.
        value_one_life_max_nc: See :attr:`value_one_life_max_vs`.
        value_one_life_max_tr: See :attr:`value_one_life_max_vs`.
        last_save: The UTC timestamp this value was last updated.
        last_save_date: String version of :attr:`last_save`.

    """

    character_id: int
    stat_name: str
    profile_id: int
    value_forever_vs: float
    value_forever_nc: float
    value_forever_tr: float
    value_monthly_vs: float
    value_monthly_nc: float
    value_monthly_tr: float
    value_weekly_vs: float
    value_weekly_nc: float
    value_weekly_tr: float
    value_daily_vs: float
    value_daily_nc: float
    value_daily_tr: float
    value_one_life_max_vs: float
    value_one_life_max_nc: float
    value_one_life_max_tr: float
    last_save: int
    last_save_date: str


class CharacterStatHistory(Ps2Data):
    """Data class for ``characters_stat_history`` payloads.

    This is a generic payload that is returned multiple times per
    character. Use the :attr:`stat_name` field to determine the
    statistic returned.

    The :attr:`character_id`, and :attr:`stat_name` fields create a
    unique composite key for the table.

    Attributes:
        character_id: The character to which this stat belongs.
        stat_name: The name of the stat returned.
        all_time: The character-wide, all time value.
        one_life_max: Highest value ever achieved without dying.
        day: Dictionary mapping days to values. Keys follow the ``d01``
            pattern.
        month: Dictionary mapping months to values. Keys follow the
            ``m01`` pattern.
        week: Dictionary mapping weeks to values. Keys follow the
            ``w01`` pattern.
        last_save: The UTC timestamp this value was last updated.
        last_save_date: String version of :attr:`last_save`.

    """

    character_id: int
    stat_name: str
    all_time: float
    one_life_max: float
    day: Dict[str, float]
    month: Dict[str, float]
    week: Dict[str, float]
    last_save: int
    last_save_date: str


class CharacterWeaponStat(Ps2Data):
    """Data class for ``characters_weapon_stat`` payloads.

    This is a generic payload that is returned multiple times per
    character. Use the :attr:`stat_name` field to determine the
    statistic returned.

    The :attr:`character_id`, :attr:`item_id`, and :attr:`stat_name`
    fields create a unique composite key for the table.

    Attributes:
        character_id: The character to which this stat belongs.
        stat_name: The name of the stat returned.
        item_id: ID of the :class:`ps2.Item` this statistic is for.
        vehicle_id: ID of the :class:`ps2.Weapon` this statistic is
            for. If zero, the item is an infantry weapon.
        value: The value of the statistic.
        last_save: The UTC timestamp this value was last updated.
        last_save_date: String version of :attr:`last_save`.

    """

    character_id: int
    stat_name: str
    item_id: int
    vehicle_id: int
    value: float
    last_save: int
    last_save_date: str


class CharacterWeaponStatByFaction(Ps2Data):
    """Data class for ``characters_weapon_stat_by_faction`` payloads.

    This is a generic payload that is returned multiple times per
    character. Use the :attr:`stat_name` field to determine the
    statistic returned.

    The :attr:`character_id`, :attr:`item_id`, and :attr:`stat_name`
    fields create a unique composite key for the table.

    Attributes:
        character_id: The character to which this stat belongs.
        stat_name: The name of the stat returned.
        item_id: ID of the :class:`ps2.Item` this statistic is for.
        vehicle_id: ID of the :class:`ps2.Weapon` this statistic is
            for. If zero, the item is an infantry weapon.
        value_vs: The value of the statistic.
        value_nc: See :attr:`value_vs`.
        value_tr: See :attr:`value_vs`.
        last_save: The UTC timestamp this value was last updated.
        last_save_date: String version of :attr:`last_save`.

    """

    character_id: int
    stat_name: str
    item_id: int
    vehicle_id: int
    value_vs: float
    value_nc: float
    value_tr: float
    last_save: int
    last_save_date: str


class SingleCharacterById(Ps2Data):
    """Data class for ``single_character_by_id`` payloads.

    This is a special payload that combines all other player statistic
    tables into one. It is not advisable to cache these payloads due to
    the large memory footprint, particularly for old characters with
    many available weapons, as each comes with its own set of stats.

    .. note::

        The character ID is not part of this inner payload and must be
        stored by the caller prior to instantiation.

    Attributes:
        stat_history: Inner dictionary containing historical stats.
            The following keys are available: ``deaths``, ``kills``,
            ``score``, ``time``, ``facility_capture``,
            ``facility_defend``, ``battle_rank``, ``certs``,
            ``medals``, and ``ribbons``.
        stat: A list of :class:`CharacterStat` instances.
        stat_by_faction: A list of :class:`CharacterStatByFaction`
            instances.
        weapon_stat: A list of :class:`CharacterWeaponStat` instances.
        weapon_stat_by_faction: A list of
            :class:`CharacterWeaponStatByFaction` instances.

    """

    class SCBIHistoricalData(Ps2Data):
        """Inner container for the ``stat_history`` sub key.

        Attributes:
            all_time: The character-wide, all time value.
            one_life_max: Highest value ever achieved without dying.
            day: Dictionary mapping days to values. Keys follow the ``d01``
                pattern.
            month: Dictionary mapping months to values. Keys follow the
                ``m01`` pattern.
            week: Dictionary mapping weeks to values. Keys follow the
                ``w01`` pattern.
            last_save: The UTC timestamp this value was last updated.
            last_save_date: String version of :attr:`last_save`.

        """

        all_time: float
        one_life_max: float
        day: Dict[str, float]
        month: Dict[str, float]
        week: Dict[str, float]
        last_save: int
        last_save_date: str

    stat_history: Dict[str, SCBIHistoricalData]
    stat: List[CharacterStat]
    stat_by_faction: List[CharacterStatByFaction]
    weapon_stat: List[CharacterWeaponStat]
    weapon_stat_by_faction: List[CharacterWeaponStatByFaction]
