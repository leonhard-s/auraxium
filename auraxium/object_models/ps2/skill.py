"""Defines skill-related data types for PlanetSide 2."""

from ..datatypes import DataType, NamedDataType
from .image import Image, ImageSet
from .item import Item
from ..misc import LocalizedString


class Skill(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A skill in PS2.

    A skill is either a certification, an ASP skill or an implant's active
    effect.

    """

    _collection = 'skill'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self._grant_item_id = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._skill_line_id = None
        self.skill_line_index = None
        self.skill_points = None

    # Define properties
    @property
    def grant_item(self):
        """The item granted by the skill."""
        return Item.get(id_=self._grant_item_id)

    @property
    def image(self):
        """The image for this skill."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set for this skill."""
        ImageSet.get(id_=self._image_set_id)

    @property
    def skill_line(self):
        """The skill line this skill belongs to."""
        SkillLine.get(id_=self._skill_line_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict['description'])
        self._grant_item_id = data_dict.get('grant_item_id')
        self._image_id = data_dict.get('image_id')
        self._image_set_id = data_dict.get('image_set_id')
        self.name = LocalizedString(data_dict['name'])
        self._skill_line_id = data_dict.get('skill_line_id')
        self.skill_line_index = data_dict.get('skill_line_index')
        self.skill_points = data_dict['skill_points']


class SkillCategory(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A skill category.

    Groups skill lines into categories. Examples include "Passive Systems",
    "Ability Slot" or "Utility Slot".

    """

    _collection = 'skill_category'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self.skill_points = None
        self._skill_set_id = None
        self.skill_set_index = None

    # Define properties
    @property
    def image(self):
        """The image for this skill category."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set for this skill category."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def skill_set(self):
        """The skill sets in this skill category."""
        return SkillSet.get(id_=self._skill_set_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict['description'])
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])
        self.skill_points = data_dict.get('skill_points')
        self._skill_set_id = data_dict.get('skill_set_id')
        self.skill_set_index = data_dict.get('skill_set_index')


class SkillLine(DataType, NamedDataType):  # pylint: disable=too-many-instance-attributes
    """A skill line.

    A list of skills that improve on one another. Examples include the Chassis
    certification lines for vehicles or the ability slot of infantry.

    """

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._skill_category_id = None
        self.skill_category_index = None
        self.skill_points = None

    # Define properties
    @property
    def image(self):
        """The image set for this skill line."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set for this skill line."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def skill_category(self):
        """The skill category for this skill line."""
        return SkillCategory.get(id_=self._skill_category_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict['description']
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])
        self._skill_category_id = data_dict['skill_category_id']
        self.skill_category_index = data_dict['skill_category_id']
        self.skill_points = data_dict.get('skill_points')


class SkillSet(DataType, NamedDataType):
    """A skill set.

    A skill set is a list of skill lines that belong to the same set. Examples
    include the Sunderer Passive Systems slot or a vehicle's weapon slot.

    """

    _collection = 'skill_set'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self._required_item_id = None
        self.skill_points = None

    # Define properties
    @property
    def image(self):
        """The image for this skill set."""
        return Image.get(id_=self._image_id)

    @property
    def image_set(self):
        """The image set for this skill set."""
        return ImageSet.get(id_=self._image_set_id)

    @property
    def required_item(self):
        """The item required to unlock this skill set."""
        return Item.get(id_=self._required_item_id)

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = LocalizedString(data_dict['description'])
        self._image_id = data_dict['image_id']
        self._image_set_id = data_dict['image_set_id']
        self.name = LocalizedString(data_dict['name'])
        self._required_item_id = data_dict['required_item_id']
        self.skill_points = data_dict.get('skill_points')
