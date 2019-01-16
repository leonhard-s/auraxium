from ..census import Query
from ..datatypes import EnumeratedDataType


class PlayerState(EnumeratedDataType):
    """A player state.

    Used to handle changing cone of fires and other fields based on what the
    player is doing.

    """

    _collection = 'player_state'

    def __init__(self, id):
        self.id = id

        # Set default values
        self.description = None

    def _populate(self, data=None):
        d = data if data != None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')


# class PlayerStateGroup(InterimDatatype):
#     """Controls CoF modifiers depending on what the player is doing.
#
#     I inferred `player_state_group_2` is a complete replacement for
#     `player_state_group`, this might require correcting if I am wrong.
#
#     """
#
#     _cache_size = 200
#     _collection = 'player_state_group_2'
#
#     def __init__(self, id):
#         self.id = id
#
#         d = Query(self.__class__, id=id, limit=10).get()
#         self.player_state =
#
#         for state in d:
#             self.player_state
#             # "player_state_group_id": "1",
#             "player_state_id": "0",
#             "can_iron_sight": "1",
#             "cof_grow_rate": "50",
#             "cof_max": "7",
#             "cof_min": "2",
#             "cof_recovery_delay_ms": "0",
#             "cof_recovery_rate": "20",
#             "cof_shots_before_penalty": "0",
#             "cof_recovery_delay_threshold": "0",
#             "cof_turn_penalty": "0"
