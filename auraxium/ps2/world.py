"""World class definition."""

import dataclasses
from typing import Any, Final, List, Optional, Union

from ..base import Named, Ps2Data
from ..census import Query
from ..client import Client
from ..request import extract_payload
from ..types import CensusData
from ..utils import LocaleData

from .zone import Zone


@dataclasses.dataclass(frozen=True)
class WorldData(Ps2Data):
    """Data class for :class:`auraxium.ps2.world.World`.

    This class mirrors the payload data returned by the API, you may
    use its attributes as keys in filters or queries.
    """

    world_id: int
    state: str
    name: LocaleData

    @classmethod
    def from_census(cls, data: CensusData) -> 'WorldData':
        return cls(
            int(data['world_id']),
            str(data['state']),
            LocaleData.from_census(data['name']))


class World(Named, cache_size=20, cache_ttu=3600.0):
    """A world (or server) in the game."""

    collection = 'world'
    data: WorldData
    id_field = 'world_id'

    @staticmethod
    def _build_dataclass(data: CensusData) -> WorldData:
        return WorldData.from_census(data)

    async def events(self, **kwargs: Any) -> List[CensusData]:
        """Return events for this world.

        This provides a REST endpoint for past alerts (MetagameEvent)
        and facility captures (FacilityCapture).

        This is always limited to at most 1000 return values. Use the
        begin and end parameters to poll more data.
        """
        collection: Final[str] = 'world_event'
        query = Query(collection, service_id=self._client.service_id, **kwargs)
        query.add_term(field=self.id_field, value=self.id)
        query.limit(1000)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection=collection)
        return data

    @classmethod
    async def get_by_name(cls, name: str, *, locale: str = 'en',
                          client: Client) -> Optional['World']:
        """Retrieve a world by name.

        This query is always case-insensitive.
        """
        # NOTE: The world collection may only be queried by the world_id field
        # due to API limitations. This method works around this by first
        # retrieving all worlds, then looking the returned list up by name.
        worlds = await cls.find(20, client=client)
        name = name.lower()
        for world in worlds:
            if world.name(locale=locale).lower() == name:
                return world
        return None

    async def map(self, zone: Union[int, Zone],
                  *args: Union[int, Zone]) -> List[CensusData]:
        """Return the map status of a given zone."""
        collection: Final[str] = 'map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        zone_ids: List[int] = [zone if isinstance(zone, int) else zone.id]
        zone_ids.extend(z if isinstance(z, int) else z.id for z in args)
        value = ','.join(str(z) for z in zone_ids)
        query.add_term(field='zone_ids', value=value)
        query.limit(3000)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection=collection)
        return data
