from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype
from .ability import Ability
from .resist import ResistType
from .target import TargetType


class Effect(InterimDatatype):
    _collection = 'effect'
    _join = ['ability', 'effect_type', 'resist_type', 'target_type']

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.ability = Ability(data.get('ability_id'),
                               data_override=data.get('ability'))
        self.duration = data.get('duration_seconds')
        self.is_drain = True if data.get('is_drain') == '1' else False
        self.resist_type = ResistType(
            data.get('resist_type_id'), data_override=data.get('resist_type'))
        self.target_type = TargetType(
            data.get('target_type_id'), data_override=data.get('target_type'))
        self.type = EffectType(data.get('effect_type_id'),
                               data_override=data.get('effect_type'))

        self.parameters = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'Effect (ID: {})'.format(self.id)


class EffectType(StaticDatatype):
    _collection = 'effect_type'

    def __init__(self, id, data_override=None):
        self.id = id

        if super().is_cached(self):  # If the object is cached, skip
            return

        data = data_override if data_override != None else super().get_data(self)

        self.description = data.get('description')
        self.parameters = {}
        for i in range(14):
            self.parameters[i] = data.get('param{}'.format(i + 1))

        super()._add_to_cache(self)  # Cache this instance for future use

    def __str__(self):
        return 'EffectType (ID: {}, Description: "{}")'.format(
            self.id, self.description)
