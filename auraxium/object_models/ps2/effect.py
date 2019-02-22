from ..datatypes import CachableDataType, EnumeratedDataType
from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(CachableDataType):
    """Represents an effect.

    An effect acts upon entities in the game world. Its most common application
    is for dealing damage to items or players.

    """

    _collection = 'effect'

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
        return Ability.get(id=self._ability_id)

    @property
    def effect_type(self):
        return EffectType.get(id=self._effect_type_id)

    @property
    def resist_type(self):
        return ResistType.get(id=self._resist_type_id)

    @property
    def target_type(self):
        return TargetType.get(id=self._target_type_id)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self._ability_id = d.get('ability_id')
        self.duration = d.get('duration_seconds')
        self._effect_type_id = d['effect_type_id']
        self.is_drain = d.get('is_drain')
        self._resist_type_id = d.get('resist_type_id')
        self._target_type_id = d.get('target_type_id')
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(13):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)


class EffectType(EnumeratedDataType):
    """A type of effect.

    The effect type contains informatino about what the "param" fields of the
    corresponding effect's purpose is.

    """

    _collection = 'effect_type'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None
        # Set default values for attributes "param1" through "param13"
        s = ''
        for i in range(14):
            s += 'self.param{} = None\n'.format(i + 1)
        exec(s)

    def populate(self, data=None):
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')
        # Set attributes "param1" through "param13"
        s = ''
        for i in range(14):
            s += 'self.param{0} = d.get(\'param{0}\')\n'.format(i + 1)
        exec(s)
