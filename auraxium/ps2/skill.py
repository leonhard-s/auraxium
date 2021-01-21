"""Skill and skill line class definitions."""

from typing import Optional

from .._base import ImageMixin, Named
from ..census import Query
from ..models import SkillData, SkillCategoryData, SkillLineData, SkillSetData
from .._proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from .item import Item

__all__ = [
    'Skill',
    'SkillCategory',
    'SkillLine',
    'SkillSet',
]


class SkillSet(Named, ImageMixin, cache_size=100, cache_ttu=60.0):
    """A skill set for a particular vehicle or class.

    Attributes:
        skill_set_id: The unique ID of this skill set.
        skill_points: (Not yet documented)
        required_item_id: The item required to unlock this skill set.
            Used to prevent buying upgrades for items the player has
            not unlocked yet.
        description: The localised description of the skill set.

    """

    collection = 'skill_set'
    data: SkillSetData
    dataclass = SkillSetData
    id_field = 'skill_set_id'

    # Type hints for data class fallback attributes
    skill_set_id: int
    skill_points: Optional[int]
    required_item_id: Optional[int]
    description: Optional[LocaleData]

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


class SkillCategory(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A skill category for a particular class or vehicle.

    Skill categories are groups like "Passive Systems" or "Performance
    Slot".

    Attributes:
        skill_category_id: The unique ID of this skill category.
        skill_set_id: The :class:`SkillCategory` this category belongs
            to.
        skill_set_index: The position of this category in the
            associated skill category.
        skill_points: The unlock cost for this skill category.
        description: The localised description for this skill category.

    """

    collection = 'skill_category'
    data: SkillCategoryData
    dataclass = SkillCategoryData
    id_field = 'skill_category_id'

    # Type hints for data class fallback attributes
    skill_category_id: int
    skill_set_id: int
    skill_set_index: int
    skill_points: int
    description: Optional[LocaleData]

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


class SkillLine(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A series of skills or certifications.

    Attributes:
        skill_line_id: The unique ID for this skill line.
        skill_points: The unlock cost for this skill line.
        skill_category_id: The :class:`SkillCategory` this skill line
            belongs to.
        skill_category_index: The index of this skill line in its
            containing skill category.
        description: The localised description for this skill line.

    """

    collection = 'skill_line'
    data: SkillLineData
    dataclass = SkillLineData
    id_field = 'skill_line_id'

    # Type hints for data class fallback attributes
    skill_line_id: int
    skill_points: int
    skill_category_id: Optional[int]
    skill_category_index: Optional[int]
    description: Optional[LocaleData]

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


class Skill(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A skill or certification unlockable by a character.

    Attributes:
        skill_id: The unique ID of this skill.
        skill_line_id: The ID of the associated :class:`SkillLine`.
        skill_line_index: The position of the skill in its skill line.
        skill_points: The unlock cost of the skill.
        grant_item_id: The :class:`~auraxium.ps2.Item` granted by this
            skill, if any.
        description: The localised description for this skill.

    """

    collection = 'skill'
    data: SkillData
    dataclass = SkillData
    id_field = 'skill_id'

    # Type hints for data class fallback attributes
    skill_id: int
    skill_line_id: int
    skill_line_index: int
    skill_points: int
    grant_item_id: Optional[int]
    description: Optional[LocaleData]

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
