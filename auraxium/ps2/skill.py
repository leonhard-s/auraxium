from ..datatypes import CachableDataType
from .image import Image, ImageSet
from .item import Item
from ..misc import LocalizedString


class Skill(CachableDataType):
    """A skill in PS2.

    A skill is either a certification, an ASP skill or an implant's active
    effect.

    """

    _collection = 'skill'

    def __init__(self, id):
        self.id = id

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
        try:
            return self._grant_item
        except AttributeError:
            self._grant_item = Item.get(id=self._grant_item_id)
            return self._grant_item

    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    @property
    def skill_line(self):
        try:
            return self._skill_line
        except AttributeError:
            self._skill_line = SkillLine.get(id=self._skill_line_id)
            return self._skill_line

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self.grant_item_id = d.get('grant_item_id')
        self.image = d.get('image_id')
        self.image_set = d.get('image_set_id')
        self.name = LocalizedString(d['name'])
        self.skill_line = d.get('skill_line_id')
        self.skill_line_index = d.get('skill_line_index')
        self.skill_points = d['skill_points']


class SkillCategory(CachableDataType):
    """A skill category.

    Groups skill lines into categories. Examples include "Passive Systems",
    "Ability Slot" or "Utility Slot".

    """

    _collection = 'skill_category'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        self._image_id = None
        self._image_set_id = None
        self.name = None
        self.skill_points = None
        self._skill_set = None
        self.skill_set_index = None

    # Define properties
    @property
    def image(self):
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    @property
    def skill_set(self):
        try:
            return self._skill_set
        except AttributeError:
            self._skill_set = ImageSet.get(id=self._skill_set_id)
            return self._skill_set

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        self.skill_points = d.get('skill_points')
        self._skill_set_id = d.get('skill_set_id')
        self.skill_set_index = d.get('skill_set_index')


class SkillLine(CachableDataType):
    """A skill line.

    A list of skills that improve on one another. Examples include the Chassis
    certification lines for vehicles or the ability slot of infantry.

    """

    def __init__(self, id):
        self.id = id

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
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    @property
    def skill_category(self):
        try:
            return self._skill_category
        except AttributeError:
            self._skill_category = SkillCategory.get(
                id=self._skill_category_id)
            return self._skill_category

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d['description']
        self.image = d['image_id']
        self.image_set = d['image_set_id']
        self.name = LocalizedString(d['name'])
        self._skill_ctegory_id = d['skill_category_id']
        self.skill_category_index = d['skill_category_id']
        self.skill_points = d.get('skill_points')


class SkillSet(CachableDataType):
    """A skill set.

    A skill set is a list of skill lines that belong to the same set. Examples
    include the Sunderer Passive Systems slot or a vehicle's weapon slot.

    """

    _collection = 'skill_set'

    def __init__(self, id):
        self.id = id

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
        try:
            return self._image
        except AttributeError:
            self._image = Image.get(id=self._image_id)
            return self._image

    @property
    def image_set(self):
        try:
            return self._image_set
        except AttributeError:
            self._image_set = ImageSet.get(id=self._image_set_id)
            return self._image_set

    @property
    def required_item(self):
        try:
            return self._required_item
        except AttributeError:
            self._required_item = Item.get(id=self._required_item_id)
            return self._required_item

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = LocalizedString(d['description'])
        self._image_id = d['image_id']
        self._image_set_id = d['image_set_id']
        self.name = LocalizedString(d['name'])
        self._required_item_id = d['required_item_id']
        self.skill_points = d.get('skill_points')
