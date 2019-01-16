from ..census import Query
from ..datatypes import CachableDataType, EnumeratedDataType
from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(CachableDataType):
    """Represents an effect.

    An effect acts upon entities in the game world. Its most common application
    is for dealing damage to items or players.

    """

    def __init__(self, id):
        self.id = id

        # Set default values
        self._ability_id = 0
        self.duration = None
        self._effect_type_id = 0
        self.is_drain = 0
        self._resist_type_id = 0
        self._target_type_id = 0
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

        # Define properties
        @property
        def ability(self):
            try:
                return self._ability
            except AttributeError:
                self._ability = Ability.get(cls=self.__class__,
                                            id=self._ability_id)
                return self._ability

        @property
        def effect_type(self):
            try:
                return self._effect_type
            except AttributeError:
                self._effect_type = EffectType.get(cls=self.__class__,
                                                   id=self._effect_type_id)
                return self._effect_type

        @property
        def resist_type(self):
            try:
                return self._resist_type
            except AttributeError:
                self._resist_type = EffectType.get(cls=self.__class__,
                                                   id=self._resist_type_id)
                return self._resist_type

        @property
        def target_type(self):
            try:
                return self._target_type
            except AttributeError:
                self._target_type = TargetType.get(id=self._target_type_id)
                return self._target_type

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.ability_id = d.get('effect_type_id')
        self.duration = d.get('duration_seconds')
        self.effect_type_id = d['effect_type_id']
        self.is_drain = d.get('is_drain')
        self.resist_type_id = d.get('resist_type_id')
        self.target_type_id = d.get('target_type_id')
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)


class EffectType(EnumeratedDataType):
    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(14):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(14):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
