"""Profile and loadout class definitions."""

from typing import Final

from ..base import Cached
from ..census import Query
from ..models import LoadoutData, ProfileData
from ..models.base import FallbackMixin
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData

from ._armour import ArmourInfo
from ._faction import Faction
from ._resist import ResistInfo

__all__ = [
    'Loadout',
    'Profile'
]


class Profile(Cached, cache_size=200, cache_ttu=60.0):
    """An entity in the game world.

    This is used to specify the resistance and armour values to
    apply to a given object.

    Profiles include faction-specific classes, vehicles, facility
    infrastructure such as turrets, generators or shields, as well as
    other non-static entities such as Cortium nodes or pumpkins.

    Attributes:
        id: The unique ID of this profile.
        description: The description of the profile.

    """

    collection = 'profile_2'
    data: ProfileData
    dataclass = ProfileData
    id_field = 'profile_id'

    # Type hints for data class fallback attributes
    id: int
    description: str

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the profile.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.set_fields(ArmourInfo.id_field)
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the profile.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.set_fields(ResistInfo.id_field)
        return SequenceProxy(ResistInfo, query, client=self._client)


class Loadout(Cached, FallbackMixin, cache_size=20, cache_ttu=3600.0):
    """Represents a faction-specific infantry class.

    Attributes:
        id: The unique ID of this loadout.
        profile_id: The ID of the associated profile.
        faction_id: The faction for this loadout.
        code_name: A string describing the loadout.

    """

    collection = 'loadout'
    data: LoadoutData
    dataclass = LoadoutData
    id_field = 'loadout_id'

    # Type hints for data class fallback attributes
    id: int
    profile_id: int
    faction_id: int
    code_name: str

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the loadout.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.set_fields(ArmourInfo.id_field)
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction of the loadout.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def profile(self) -> InstanceProxy[Profile]:
        """Return the profile of the loadout.

        This returns an :class:`auraxium.InstanceProxy`.
        """
        query = Query(Profile.collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        return InstanceProxy(Profile, query, client=self._client)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the loadout.

        This returns a :class:`auraxium.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.set_fields(ResistInfo.id_field)
        return SequenceProxy(ResistInfo, query, client=self._client)

    @staticmethod
    def fallback_hook(id_: int) -> CensusData:
        if id_ not in (*range(28, 33), 45):
            raise KeyError(f'No fallback value for D {id_}')
        profile_id = id_ + 162 if id_ != 45 else 252
        code_name = {
            28: 'NSO Infiltrator',
            29: 'NSO Light Assault',
            30: 'NSO Medic',
            31: 'NSO Engineer',
            32: 'NSO Heavy Assault',
            45: 'NSO MAX'}
        # TODO: Switch to returning data model
        return {'loadout_id': id_,
                'profile_id': profile_id,
                'faction_id': 4,
                'code_name': code_name[id_]}
