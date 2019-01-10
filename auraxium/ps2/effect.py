from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(InterimDatatype):
    _collection = 'effect'

    def __init__(self, id):
        self.id = id
        data = super(Effect, self).get_data(self)

        self.ability = Ability(data.get('ability_id'))
        self.duration = data.get('duration_seconds')
        self.is_drain = True if data.get('is_drain') == '1' else False
        self.resist_type = ResistType(data.get('resist_type_id'))
        self.target_type = TargetType(data.get('target_type_id'))
        self.type = EffectType(data.get('effect_type_id'))

        self.parameters = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))


class EffectType(StaticDatatype):
    _collection = 'effect_type'

    def __init__(self, id):
        self.id = id
        data = super(EffectType, self).get_data(self)

        self.description = data.get('description')
        self.parameters = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))
