"""Profile and loadout class definitions."""

import dataclasses
from typing import Final, Optional

from ..base import Named, Cached, Ps2Data
from ..census import Query
from ..proxy import InstanceProxy, SequenceProxy
from ..types import CensusData
from ..utils import LocaleData, optional

from .armour import ArmourInfo
from .faction import Faction
from .resist import ResistInfo


@dataclasses.dataclass(frozen=True)
class ProfileData(Ps2Data):
    """Data class for :class:`auraxium.ps2.profile.Profile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    profile_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ProfileData':
        return cls(
            int(data['profile_id']),
            str(data['description']))


class Profile(Cached, cache_size=200, cache_ttu=60.0):
    """An entity in the game world.

    This is used to specify the resistance and armour values to
    apply to a given object.

    Profiles include faction-specific classes, vehicles, facility
    infrastructure such as turrets, generators or shields, as well as
    other non-static entities such as Cortium nodes or pumpkins.
    """

    collection = 'profile_2'
    data: ProfileData
    id_field = 'profile_id'

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the profile.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.parent_field = join.child_field = ArmourInfo.id_field
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def _build_dataclass(self, data: CensusData) -> ProfileData:
        return ProfileData.from_census(data)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the profile.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.parent_field = join.child_field = ResistInfo.id_field
        return SequenceProxy(ResistInfo, query, client=self._client)


@dataclasses.dataclass(frozen=True)
class LoadoutData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Loadout`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    loadout_id: int
    profile_id: int
    faction_id: int
    code_name: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'LoadoutData':
        return cls(
            int(data['loadout_id']),
            int(data['profile_id']),
            int(data['faction_id']),
            str(data['code_name']))


class Loadout(Cached, cache_size=20, cache_ttu=3600.0):
    """Represents a faction-specific infantry class."""

    collection = 'loadout'
    data: LoadoutData
    id_field = 'loadout_id'

    def _build_dataclass(self, data: CensusData) -> LoadoutData:
        return LoadoutData.from_census(data)

    def armour_info(self) -> SequenceProxy[ArmourInfo]:
        """Return the armour info of the loadout.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_armor_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(20)
        join = query.create_join(ArmourInfo.collection)
        join.parent_field = join.child_field = ArmourInfo.id_field
        return SequenceProxy(ArmourInfo, query, client=self._client)

    def faction(self) -> InstanceProxy[Faction]:
        """Return the faction of the loadout.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Faction.collection, service_id=self._client.service_id)
        query.add_term(field=Faction.id_field, value=self.data.faction_id)
        return InstanceProxy(Faction, query, client=self._client)

    def profile(self) -> InstanceProxy[Profile]:
        """Return the profile of the loadout.

        This returns an :class:`auraxium.proxy.InstanceProxy`.
        """
        query = Query(Profile.collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        return InstanceProxy(Profile, query, client=self._client)

    def resist_info(self) -> SequenceProxy[ResistInfo]:
        """Return the resist info of the loadout.

        This returns a :class:`auraxium.proxy.SequenceProxy`.
        """
        collection: Final[str] = 'profile_resist_map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=Profile.id_field, value=self.data.profile_id)
        query.limit(500)
        join = query.create_join(ResistInfo.collection)
        join.parent_field = join.child_field = ResistInfo.id_field
        return SequenceProxy(ResistInfo, query, client=self._client)
