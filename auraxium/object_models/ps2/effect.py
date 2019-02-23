from typing import List

from ..datatypes import DataType
from ..typing import Param


from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(DataType):
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
        return Ability.get(id_=self._ability_id)

    @property
    def effect_type(self):
        return EffectType.get(id_=self._effect_type_id)

    @property
    def resist_type(self):
        return ResistType.get(id_=self._resist_type_id)

    @property
    def target_type(self):
        return TargetType.get(id_=self._target_type_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self._ability_id = d.get('ability_id')
        self.duration = d.get('duration_seconds')
        self._effect_type_id = d['effect_type_id']
        self.is_drain = d.get('is_drain')
        self._resist_type_id = d.get('resist_type_id')
        self._target_type_id = d.get('target_type_id')

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
        d = data if data is not None else super()._get_data(self.id_)

        # Set attribute values
        self.description = d.get('description')

        self.param = [d['param' + str(i + 1)] if d.get('param' + str(i + 1))
                      is not None else None for i in range(13)]
