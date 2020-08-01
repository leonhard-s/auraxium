"""Skill and skill line class definitions."""

import dataclasses
from typing import Optional

from ..base import Named, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .item import Item


@dataclasses.dataclass(frozen=True)
class SkillSetData(Ps2Data):
    """Data class for :class:`auraxium.ps2.skill.SkillSet`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class SkillSet(Named, cache_size=100, cache_ttu=60.0):
    """A skill set for a particular vehicle or class."""

    collection = 'skill_set'
    data: SkillSetData
    id_field = 'skill_set_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> SkillSetData:
        return SkillSetData.from_census(data)

    def categories(self) -> SequenceProxy['SkillCategory']:
        """Return the skill categories in this skill set.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(
            SkillCategory.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100)
        return SequenceProxy(SkillCategory, query, client=self._client)

    def required_item(self) -> InstanceProxy[Item]:
        """Return the item required for access to this skill set.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        item_id = self.data.required_item_id or -1
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item_id)
        return InstanceProxy(Item, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class SkillCategoryData(Ps2Data):
    """Data class for :class:`auraxium.ps2.skill.SkillCategory`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class SkillCategory(Named, cache_size=50, cache_ttu=60.0):
    """A skill category for a particular class or vehicle.

    Skill categories are groups like "Passive Systems" or "Performance
    Slot".
    """

    collection = 'skill_category'
    data: SkillCategoryData
    id_field = 'skill_category_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> SkillCategoryData:
        return SkillCategoryData.from_census(data)

    def skill_lines(self) -> SequenceProxy['SkillLine']:
        """Return the skill lines contained in this category.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(SkillLine.collection, service_id=self._client.service_id)
        query.add_term(field=SkillCategory.id_field, value=self.id)
        query.sort('skill_category_index')
        return SequenceProxy(SkillLine, query, client=self._client)

    def skill_set(self) -> InstanceProxy['SkillSet']:
        """Return the skill set for this category.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(SkillSet.collection, service_id=self._client.service_id)
        query.add_term(field=SkillSet.id_field, value=self.data.skill_set_id)
        return InstanceProxy(SkillSet, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class SkillLineData(Ps2Data):
    """Data class for :class:`auraxium.ps2.skill.SkillLine`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class SkillLine(Named, cache_size=50, cache_ttu=60.0):
    """A series of skills or certifications."""

    collection = 'skill_line'
    data: SkillLineData
    id_field = 'skill_line_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> SkillLineData:
        return SkillLineData.from_census(data)

    def category(self) -> InstanceProxy[SkillCategory]:
        """Return the category this skill line belongs to.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        category_id = self.data.skill_category_id or -1
        query = Query(
            SkillCategory.collection, service_id=self._client.service_id)
        query.add_term(field=SkillCategory.id_field, value=category_id)
        return InstanceProxy(SkillCategory, query, client=self._client)

    def skills(self) -> SequenceProxy['Skill']:
        """Return the skills contained in this skill line in order.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        query = Query(Skill.collection, service_id=self._client.service_id)
        query.add_term(field=SkillLine.id_field, value=self.id)
        query.limit(20)
        query.sort('skill_line_index')
        return SequenceProxy(Skill, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class SkillData(Ps2Data):
    """Data class for :class:`auraxium.ps2.skill.Skill`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
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


class Skill(Named, cache_size=50, cache_ttu=60.0):
    """A skill or certification unlockable by a character."""

    collection = 'skill'
    data: SkillData
    id_field = 'skill_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> SkillData:
        return SkillData.from_census(data)

    def grant_item(self) -> InstanceProxy[Item]:
        """Return the item unlocked by this skill.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        item_id = self.data.grant_item_id or -1
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item_id)
        return InstanceProxy(Item, query, self._client)

    def skill_line(self) -> InstanceProxy[SkillLine]:
        """Return the skill line containing this skill.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(SkillLine.collection, service_id=self._client.service_id)
        query.add_term(field=SkillLine.id_field, value=self.data.skill_line_id)
        return InstanceProxy(SkillLine, query, self._client)
