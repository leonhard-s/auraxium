"""World class definition."""

import datetime
from typing import Any, Final

from ..base import Named, NamedT
from ..census import Query
from ..collections import WorldData
from .._rest import RequestClient, extract_payload, extract_single
from ..types import CensusData, LocaleData

from ._zone import Zone

__all__ = [
    'World'
]


class World(Named, cache_size=20, cache_ttu=3600.0):
    """A world (or server) in the game.

    .. attribute:: id
       :type: int

       The unique ID of the world. In the API payload, this field
       is called ``world_id``.

    .. attribute:: name
       :type: auraxium.types.LocaleData

       Localised name of the world.

    .. attribute:: state
       :type: str

       The current state (i.e. online status) of the world.

    .. attribute:: description
       :type: auraxium.types.LocaleData | None

       A description of the world's server region.
    """

    collection = 'world'
    data: WorldData
    id_field = 'world_id'
    _model = WorldData

    # Type hints for data class fallback attributes
    id: int
    name: LocaleData
    state: str
    description: LocaleData | None

    async def events(self, **kwargs: Any) -> list[CensusData]:
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

    async def map(self, zone: int | Zone,
                  *args: int | Zone) -> list[CensusData]:
        """Return the map status of a given zone."""
        collection: Final[str] = 'map'
        query = Query(collection, service_id=self._client.service_id)
        query.add_term(field=self.id_field, value=self.id)
        zone_ids: list[int] = [zone if isinstance(zone, int) else zone.id]
        zone_ids.extend(z if isinstance(z, int) else z.id for z in args)
        value = ','.join(str(z) for z in zone_ids)
        query.add_term(field='zone_ids', value=value)
        query.limit(3000)
        payload = await self._client.request(query)
        data = extract_payload(payload, collection=collection)
        return data

    async def status(self) -> tuple[str, datetime.datetime]:
        """Return the online status for the world.

        This returns a tuple consisting of the reported server state
        (e.g. "locked", "low", or "high", the latter referring to
        population numbers), and the last time this value was updated.
        """
        assert self.data.name is not None
        query = Query('game_server_status', namespace='global',
                      service_id=self._client.service_id, game_code='ps2',
                      name=f'^{self.data.name.en}')
        payload = await self._client.request(query)
        data = extract_single(payload, 'game_server_status')
        status = str(data['last_reported_state'])
        last_updated = int(str(data['last_reported_time']))
        return status, datetime.datetime.fromtimestamp(
            last_updated, datetime.timezone.utc)
