"""Fire modes and group class definitions."""

import enum
from typing import Dict, Final

from ..base import Cached
from ..census import Query
from ..models import FireGroupData, FireModeData
from ..proxy import InstanceProxy, SequenceProxy
from ..request import extract_payload

from .projectile import Projectile
from .states import PlayerState, PlayerStateGroup


class FireModeType(enum.IntEnum):
    """A type of fire mode.

    This is mostly used to group similar fire modes together when
    tabulating multiple weapons.
    """

    PROJECTILE = 0
    IRON_SIGHT = 1
    MELEE = 3
    TRIGGER_ITEM_ABILITY = 8
    THROWN = 12


class FireMode(Cached, cache_size=10, cache_ttu=3600.0):
    """A fire mode of a weapon.

    This class defines the bulk of a weapon's stats, such as reload
    times or accuracy.

    Note that this is not synonymous with in-game fire modes, these are
    handled by the :class:`FireGroup` class instead. Fire groups are
    also used to implement the auxiliary under-barrel fire modes.

    Implementation detail: This class wraps the ``fire_mode_2``
    collection, the regular ``fire_mode`` collection does not have a
    representation in the object model.
    """

    collection = 'fire_mode_2'
    data: FireModeData
    dataclass = FireModeData
    id_field = 'fire_mode_id'

    @property
    def type(self) -> FireModeType:
        """Return the type of fire mode as an enum."""
        return FireModeType(self.data.fire_mode_type_id)

    async def state_groups(self) -> Dict[PlayerState, PlayerStateGroup]:
        """Return the state-specific data for a fire mode."""
        collection: Final[str] = 'player_state_group_2'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field='player_state_group_id',
                       value=self.data.player_state_group_id)
        query.limit(10)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection)
        states: Dict[PlayerState, PlayerStateGroup] = {}
        for group_data in data:
            group = PlayerStateGroup(**group_data)
            state = PlayerState(group.player_state_id)
            states[state] = group
        return states

    def projectile(self) -> InstanceProxy[Projectile]:
        """Return the projectile associated with this fire mode."""
        collection: Final[str] = 'fire_mode_to_projectile'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        join = query.create_join(Projectile.collection)
        join.set_fields(Projectile.id_field)
        return InstanceProxy(Projectile, query, client=self._client)


class FireGroup(Cached, cache_size=10, cache_ttu=60.0):
    """Links multiple fire modes into a group.

    Fire groups are comparable to the in-game fire modes, such as
    burst, semi auto or fully automatic. They are also used to
    implement auxiliary fire modes such as under-barrel launchers.
    """

    collection = 'fire_group'
    data: FireGroupData
    dataclass = FireGroupData
    id_field = 'fire_group_id'

    def fire_modes(self) -> SequenceProxy[FireMode]:
        """Return the fire modes in the fire group."""
        collection: Final[str] = 'fire_group_to_fire_mode'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(FireMode.collection)
        join.set_fields(FireMode.id_field)
        return SequenceProxy(FireMode, query, client=self._client)
