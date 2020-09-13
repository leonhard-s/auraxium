"""Data classes for :mod:`auraxium.ps2.skill`."""

import dataclasses
from typing import Optional

from ..base import Ps2Data
from ..types import CensusData
from ..utils import LocaleData, optional


__all__ = [
    'SkillData',
    'SkillCategoryData',
    'SkillLineData',
    'SkillSetData'
]


@dataclasses.dataclass(frozen=True)
class SkillData(Ps2Data):
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
        image_set_id: The image set for this skill.
        image_id: The default image asset for this skill.
        image_path: The path to the default image asset for this skill.

    """

    skill_id: int
    skill_line_id: int
    skill_line_index: int
    skill_points: int
    grant_item_id: Optional[int]
    name: LocaleData
    description: LocaleData
    image_set_id: Optional[int]
    image_id: Optional[int]
    image_path: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'SkillData':
        return cls(
            int(data['skill_id']),
            int(data['skill_line_id']),
            int(data['skill_line_index']),
            int(data['skill_points']),
            optional(data, 'grant_item_id', int),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))


@dataclasses.dataclass(frozen=True)
class SkillCategoryData(Ps2Data):
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
        image_set_id: The image set for this skill category.
        image_id: The default image asset for this skill category.
        image_path: The path to the default image asset for this skill
            category.

    """

    skill_category_id: int
    skill_set_id: int
    skill_set_index: int
    skill_points: int
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'SkillCategoryData':
        if 'description' in data:
            description = LocaleData.from_census(data['description'])
        else:
            description = LocaleData.empty()
        return cls(
            int(data['skill_category_id']),
            int(data['skill_set_id']),
            int(data['skill_set_index']),
            int(data['skill_points']),
            LocaleData.from_census(data['name']),
            description,
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


@dataclasses.dataclass(frozen=True)
class SkillLineData(Ps2Data):
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
        image_set_id: The image set for this skill line.
        image_id: The default image asset for this skill line.
        image_path: The path to the default image asset for this skill
            line.

    """

    skill_line_id: int
    skill_points: int
    skill_category_id: Optional[int]
    skill_category_index: Optional[int]
    name: LocaleData
    description: LocaleData
    image_set_id: int
    image_id: int
    image_path: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'SkillLineData':
        return cls(
            int(data['skill_line_id']),
            int(data['skill_points']),
            optional(data, 'skill_category_id', int),
            optional(data, 'skill_category_index', int),
            LocaleData.from_census(data['name']),
            LocaleData.from_census(data['description']),
            int(data['image_set_id']),
            int(data['image_id']),
            str(data['image_path']))


@dataclasses.dataclass(frozen=True)
class SkillSetData(Ps2Data):
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
        image_set_id: The image set for this skill set.
        image_id: The default image asset for this skill set.
        image_path: The path to the default image asset for this skill
            set.

    """

    skill_set_id: int
    skill_points: Optional[int]
    required_item_id: Optional[int]
    name: LocaleData
    description: LocaleData
    image_set_id: Optional[int]
    image_id: Optional[int]
    image_path: Optional[str]

    @classmethod
    def from_census(cls, data: CensusData) -> 'SkillSetData':
        if 'description' in data:
            description = LocaleData.from_census(data['description'])
        else:
            description = LocaleData.empty()
        return cls(
            int(data['skill_set_id']),
            optional(data, 'skill_points', int),
            optional(data, 'required_item_id', int),
            LocaleData.from_census(data['name']),
            description,
            optional(data, 'image_set_id', int),
            optional(data, 'image_id', int),
            optional(data, 'image_path', str))
