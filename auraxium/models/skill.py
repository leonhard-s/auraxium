"""Data classes for :mod:`auraxium.ps2.skill`."""

from typing import Optional

from ..base import ImageData, Ps2Data
from ..types import LocaleData


__all__ = [
    'SkillData',
    'SkillCategoryData',
    'SkillLineData',
    'SkillSetData'
]

# pylint: disable=too-few-public-methods


class SkillData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.skill.Skill`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        skill_id: The unique ID of this skill.
        skill_line_id: The ID of the associated :class:`SkillLine`.
        skill_line_index: The position of the skill in its skill line.
        skill_points: The unlock cost of the skill.
        grant_item_id: The :class:`~auraxium.ps2.Item` granted by this
            skill, if any.
        name: The localised name of this skill.
        description: The localised description for this skill.

    """

    skill_id: int
    skill_line_id: int
    skill_line_index: int
    skill_points: int
    grant_item_id: Optional[int] = None
    name: LocaleData
    description: Optional[LocaleData] = None


class SkillCategoryData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.skill.SkillCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        skill_category_id: The unique ID of this skill category.
        skill_set_id: The :class:`SkillCategory` this category belongs
            to.
        skill_set_index: The position of this category in the
            associated skill category.
        skill_points: The unlock cost for this skill category.
        name: The localised name of this skill category.
        description: The localised description for this skill category.

    """

    skill_category_id: int
    skill_set_id: int
    skill_set_index: int
    skill_points: int
    name: LocaleData
    description: Optional[LocaleData] = None


class SkillLineData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.skill.SkillLine`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        skill_line_id: The unique ID for this skill line.
        skill_points: The unlock cost for this skill line.
        skill_category_id: The :class:`SkillCategory` this skill line
            belongs to.
        skill_category_index: The index of this skill line in its
            containing skill category.
        name: The localised name of this skill line.
        description: The localised description for this skill line.

    """

    skill_line_id: int
    skill_points: int
    skill_category_id: Optional[int] = None
    skill_category_index: Optional[int] = None
    name: LocaleData
    description: Optional[LocaleData] = None


class SkillSetData(Ps2Data, ImageData):
    """Data class for :class:`auraxium.ps2.skill.SkillSet`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        skill_set_id: The unique ID of this skill set.
        skill_points: (Not yet documented)
        required_item_id: The item required to unlock this skill set.
            Used to prevent buying upgrades for items the player has
            not unlocked yet.
        name: The localised name of the skill set.
        description: The localised description of the skill set.

    """

    skill_set_id: int
    skill_points: Optional[int] = None
    required_item_id: Optional[int] = None
    name: LocaleData
    description: Optional[LocaleData] = None
