"""Data classes for :mod:`auraxium.ps2.profile`."""

import dataclasses

from ..base import Ps2Data
from ..types import CensusData

__all__ = [
    'LoadoutData',
    'ProfileData'
]


@dataclasses.dataclass(frozen=True)
class LoadoutData(Ps2Data):
    """Data class for :class:`auraxium.ps2.ability.Loadout`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        loadout_id: The unique ID of this loadout.
        profile_id: The ID of the associated profile.
        faction_id: The faction for this loadout.
        code_name: A string describing the loadout.

    """

    loadout_id: int
    profile_id: int
    faction_id: int
    code_name: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'LoadoutData':
        return cls(
            int(data.pop('loadout_id')),
            int(data.pop('profile_id')),
            int(data.pop('faction_id')),
            str(data.pop('code_name')))


@dataclasses.dataclass(frozen=True)
class ProfileData(Ps2Data):
    """Data class for :class:`auraxium.ps2.profile.Profile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.

    Attributes:
        profile_id: The unique ID of this profile.
        description: The description of the profile.

    """

    profile_id: int
    description: str

    @classmethod
    def from_census(cls, data: CensusData) -> 'ProfileData':
        return cls(
            int(data.pop('profile_id')),
            str(data.pop('description')))
