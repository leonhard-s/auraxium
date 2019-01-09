from ..census import Query
from ..datatypes import InterimDatatype, StaticDatatype

# from .ability import Ability
# from .resist import ResistType
# from .target import TargetType


class Effect(InterimDatatype):
    _collection = 'effect'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        try:
            # self.ability = Ability(data['ability_id'])
            self.ability = None
        except KeyError:
            self.ability = None

        try:
            self.duration = int(data['duration_seconds'])
        except KeyError:
            self.duration = -1

        try:
            self.is_drain = True if data['is_drain'] == 1 else False
        except KeyError:
            self.is_drain = False

        # self.resist_type = ResistType(data['resist_type_id'])
        # self.target_type = TargetType(data['target_type_id'])
        self.type = EffectType(data['effect_type_id'])

        self.parameters = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass


class EffectType(StaticDatatype):
    _collection = 'effect_type'

    def __init__(self, id):
        self.id = id

        data = Query(self.__class__, id=id).get_single()

        self.description = data['description']

        self.parameters = {}
        for i in range(14):
            try:
                self.parameters[i] = data['param{}'.format(i + 1)]
            except KeyError:
                pass
