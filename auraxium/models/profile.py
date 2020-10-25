"""Data classes for :mod:`auraxium.ps2.profile`."""

from ..base import Ps2Data

__all__ = [
    'LoadoutData',
    'ProfileData'
]


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
