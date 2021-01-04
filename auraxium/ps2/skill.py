"""Skill and skill line class definitions."""

from ..base import ImageMixin, Named
from ..census import Query
from ..models import SkillData, SkillCategoryData, SkillLineData, SkillSetData
from ..proxy import InstanceProxy, SequenceProxy

from .item import Item


class SkillSet(Named, ImageMixin, cache_size=100, cache_ttu=60.0):
    """A skill set for a particular vehicle or class."""

    collection = 'skill_set'
    data: SkillSetData
    dataclass = SkillSetData
    id_field = 'skill_set_id'

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
    """

    collection = 'skill_category'
    data: SkillCategoryData
    dataclass = SkillCategoryData
    id_field = 'skill_category_id'

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
    """A series of skills or certifications."""

    collection = 'skill_line'
    data: SkillLineData
    dataclass = SkillLineData
    id_field = 'skill_line_id'

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
    """A skill or certification unlockable by a character."""

    collection = 'skill'
    data: SkillData
    dataclass = SkillData
    id_field = 'skill_id'

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
