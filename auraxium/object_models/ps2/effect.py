"""Defines effect-related data types for PlanetSide 2."""

from typing import List

from ..datatypes import DataType
from ..typing import Param


from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(DataType):  # pylint: disable=too-many-instance-attributes
    """Represents an effect.

    An effect acts upon entities in the game world. Its most common application
    is for dealing damage to items or players.

    """

    _collection = 'effect'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self._ability_id = 0
        self.duration = None
        self._effect_type_id = 0
        self.is_drain = 0
        self._resist_type_id = 0
        self._target_type_id = 0

        self.param: List[Param] = [None for i in range(13)]

    # Define properties
    @property
    def ability(self):
        """The Ability for the effect."""
        return Ability.get(id_=self._ability_id)

    @property
    def effect_type(self):
        """The type of effect."""
        return EffectType.get(id_=self._effect_type_id)

    @property
    def resist_type(self):
        """The ResistType used by the effect."""
        return ResistType.get(id_=self._resist_type_id)

    @property
    def target_type(self):
        """The TargetType used by the effect."""
        return TargetType.get(id_=self._target_type_id)

    def populate(self, data=None):
        """Populates the object with data."""
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._ability_id = data_dict.get('ability_id')
        self.duration = data_dict.get('duration_seconds')
        self._effect_type_id = data_dict['effect_type_id']
        self.is_drain = data_dict.get('is_drain')
        self._resist_type_id = data_dict.get('resist_type_id')
        self._target_type_id = data_dict.get('target_type_id')

        self.param: List[Param] = [None for i in range(13)]


class EffectType(DataType):
    """A type of effect.

    The effect type contains informatino about what the "param" fields of the
    corresponding effect's purpose is.

    """

    _collection = 'effect_type'

    def __init__(self, id_):
        self.id_ = id_

        # Set default values
        self.description = None

        self.param: List[Param] = [None for i in range(13)]

    def populate(self, data=None):
        data_dict = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = data_dict.get('description')

        self.param = [data_dict['param' + str(i + 1)] if data_dict.get('param' + str(i + 1))
                      is not None else None for i in range(13)]
