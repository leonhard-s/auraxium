from ...base_api import Query
from ..datatypes import CachableDataType, EnumeratedDataType


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
        d = data if data is not None else super()._get_data(self.id)

        # Set attribute values
        self.description = d.get('description')


class PlayerStateGroup(CachableDataType):
    """Controls CoF modifiers depending on what the player is doing.

    I inferred `player_state_group_2` is a complete replacement for
    `player_state_group`, this might require correcting if I am wrong.

    """

    _collection = 'player_state_group_2'
    _id_field = 'player_state_group_id'

    def __init__(self, id):
        self.id = id

        # Set default values
        self._player_states = None  # Internal (See properties)

    # Define properties
    @property
    def player_states(self):
        try:
            return self._player_states
        except AttributeError:
            data = Query('player_state_group_2', player_state_group_id=self.id).limit(6).get()
            self._player_states = [PlayerStateGroupEntry(data=ps) for ps in data]
            self._player_states.sort(key=lambda ps: ps.player_state_id)
            return self._player_states


class PlayerStateGroupEntry():
    """An entry within a player state group."""

    def __init__(self, data):
        # Set attribute values
        self.can_iron_sight = data.get('can_iron_sight')
        self.cof_grow_rate = data.get('cof_grow_rate')  # bloom?
        self.cof_max = data.get('cof_max')
        self.cof_min = data.get('cof_min')
        self.cof_recovery_delay = data.get('cof_recovery_delay')
        self.cof_recovery_rate = data.get('cof_recovery_rate')
        self.cof_shots_before_penalty = data.get('cof_shots_before_penalty')
        self.cof_recovery_delay_threshold = data.get(
            'cof_recovery_delay_threshold')
        self.cof_turn_penalty = data.get('cof_turn_penalty')
        self.player_state_id = data.get('player_state_id')

    @property
    def player_state(self):
        return PlayerState.get(id=self.player_state_id)
