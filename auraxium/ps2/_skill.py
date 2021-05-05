"""Skill and skill line class definitions."""

from typing import Optional

from ..base import ImageMixin, Named
from ..census import Query
from ..models import SkillData, SkillCategoryData, SkillLineData, SkillSetData
from .._proxy import InstanceProxy, SequenceProxy
from ..types import LocaleData

from ._item import Item

__all__ = [
    'Skill',
    'SkillCategory',
    'SkillLine',
    'SkillSet',
]


class SkillSet(Named, ImageMixin, cache_size=100, cache_ttu=60.0):
    """A skill set for a particular vehicle or class.

    In the old certifications menu, skill sets were used for all
    certifications associated with a given item or vehicle. Since its
    removal, they are mostly for internal grouping of skill lines.

    Additionally, skill sets are used for unlocking vehicle weapons.

    .. attribute:: id
       :type: int

       The unique ID of this skill set. In the API payload, this
       field is called ``reward_type_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the skill set.

    .. attribute:: skill_points
       :type: int | None

       The number of certification points required to unlock a given
       vehicle weapon.

    .. attribute:: required_item_id
       :type: int | None

       The :class:`~auraxium.ps2.Item` required to unlock this skill
       set. Used to prevent buying upgrades for items the player has
       not unlocked yet.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description of the skill set.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'skill_set'
    data: SkillSetData
    id_field = 'skill_set_id'
    _model = SkillSetData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    skill_points: Optional[int]
    required_item_id: Optional[int]
    description: Optional[LocaleData]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def categories(self) -> SequenceProxy['SkillCategory']:
        """Return the skill categories in this skill set.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(
            SkillCategory.collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(100)
        return SequenceProxy(SkillCategory, query, client=self._client)

    def required_item(self) -> InstanceProxy[Item]:
        """Return the item required for access to this skill set.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        item_id = self.data.required_item_id or -1
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item_id)
        return InstanceProxy(Item, query, client=self._client)


class SkillCategory(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A skill category for a particular class or vehicle.

    Skill categories are groups like "Passive Systems", "Performance
    Slot", or weapon-specific groups like scopes or rail attachments.

    .. attribute:: id
       :type: int

       The unique ID of this skill category. In the API payload, this
       field is called ``skill_category_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the skill category.

    .. attribute:: skill_set_id
       :type: int

       The :class:`~auraxium.ps2.SkillCategory` this category belongs
       to.

       .. seealso::

          :meth:`skill_set` -- The skill set containing this skill
          category.

    .. attribute:: skill_set_index
       :type: int

       The position of this category in the associated skill category.

    .. attribute:: skill_points
       :type: int

       Unused.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description for this skill category.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'skill_category'
    data: SkillCategoryData
    id_field = 'skill_category_id'
    _model = SkillCategoryData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    skill_set_id: int
    skill_set_index: int
    skill_points: int
    description: Optional[LocaleData]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def skill_lines(self) -> SequenceProxy['SkillLine']:
        """Return the skill lines contained in this category.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(SkillLine.collection, service_id=self._client.service_id)
        query.add_term(field=SkillCategory.id_field, value=self.id)
        query.sort('skill_category_index')
        return SequenceProxy(SkillLine, query, client=self._client)

    def skill_set(self) -> InstanceProxy['SkillSet']:
        """Return the skill set for this category.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(SkillSet.collection, service_id=self._client.service_id)
        query.add_term(field=SkillSet.id_field, value=self.data.skill_set_id)
        return InstanceProxy(SkillSet, query, client=self._client)


class SkillLine(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A series of skills or certifications.

    .. attribute:: id
       :type: int

       The unique ID for this skill line. In the API payload, this
       field is called ``skill_line_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the skill line.

    .. attribute:: skill_points
       :type: int

       Unused. Any skill lines that can be acquired in-game have a cost
       of zero. Skill lines with non-zero cost are unused and have
       costs of 999'999.

    .. attribute:: skill_category_id
       :type: int | None

       The :class:`~auraxium.ps2.SkillCategory` this skill line belongs
       to.

       .. seealso::

          :meth:`category` -- The skill set category containing this
          skill line.

    .. attribute:: skill_category_index
       :type: int | None

       The index of this skill line in its containing skill category.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description for this skill line.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'skill_line'
    data: SkillLineData
    id_field = 'skill_line_id'
    _model = SkillLineData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    skill_points: int
    skill_category_id: Optional[int]
    skill_category_index: Optional[int]
    description: Optional[LocaleData]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def category(self) -> InstanceProxy[SkillCategory]:
        """Return the category this skill line belongs to.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        category_id = self.data.skill_category_id or -1
        query = Query(
            SkillCategory.collection, service_id=self._client.service_id)
        query.add_term(field=SkillCategory.id_field, value=category_id)
        return InstanceProxy(SkillCategory, query, client=self._client)

    def skills(self) -> SequenceProxy['Skill']:
        """Return the skills contained in this skill line in order.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        query = Query(Skill.collection, service_id=self._client.service_id)
        query.add_term(field=SkillLine.id_field, value=self.id)
        query.limit(20)
        query.sort('skill_line_index')
        return SequenceProxy(Skill, query, client=self._client)


class Skill(Named, ImageMixin, cache_size=50, cache_ttu=60.0):
    """A skill or certification unlockable by a character.

    .. attribute:: id
       :type: int

       The unique ID of this skill. In the API payload, this
       field is called ``skill_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the skill.

    .. attribute:: skill_line_id
       :type: int

       The ID of the associated :class:`~auraxium.ps2.SkillLine`.

       .. seealso::

          :meth:`skill_line` -- The skill line containing this skill.

    .. attribute:: skill_line_index
       :type: int

       The position of the skill in its skill line.

    .. attribute:: skill_points
       :type: int

       The unlock cost of the skill.

    .. attribute:: grant_item_id
       :type: int | None

       The :class:`~auraxium.ps2.Item` granted by this skill, if any.

       .. seealso::

          :meth:`grant_item` -- The item granted by this skill.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       The localised description for this skill.

    .. attribute:: image_id
       :type: int | None

       The image ID of the default image.

    .. attribute:: image_set_id
       :type: int | None

       The corresponding image set.

    .. attribute:: image_path
       :type: str | None

       The base path to the image with the default :attr:`image_id`.
    """

    collection = 'skill'
    data: SkillData
    id_field = 'skill_id'
    _model = SkillData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    skill_line_id: int
    skill_line_index: int
    skill_points: int
    grant_item_id: Optional[int]
    description: Optional[LocaleData]
    image_id: Optional[int]
    image_set_id: Optional[int]
    image_path: Optional[str]

    def grant_item(self) -> InstanceProxy[Item]:
        """Return the item unlocked by this skill.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        item_id = self.data.grant_item_id or -1
        query = Query(Item.collection, service_id=self._client.service_id)
        query.add_term(field=Item.id_field, value=item_id)
        return InstanceProxy(Item, query, self._client)

    def skill_line(self) -> InstanceProxy[SkillLine]:
        """Return the skill line containing this skill.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(SkillLine.collection, service_id=self._client.service_id)
        query.add_term(field=SkillLine.id_field, value=self.data.skill_line_id)
        return InstanceProxy(SkillLine, query, self._client)
