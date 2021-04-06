"""Data classes for :mod:`auraxium.ps2.profile`."""

from ._base import RESTPayload

__all__ = [
    'LoadoutData',
    'ProfileData'
]

# pylint: disable=too-few-public-methods


class LoadoutData(RESTPayload):
    """Data class for :class:`auraxium.ps2.ability.Loadout`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    loadout_id: int
    profile_id: int
    faction_id: int
    code_name: str


class ProfileData(RESTPayload):
    """Data class for :class:`auraxium.ps2.profile.Profile`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    profile_id: int
    description: str
