"""Third-party community endpoints compatible with Auraxium."""

import yarl

# Daybreak Game Company Census API
#
# Info: <http://census.daybreakgames.com/>
DBG_CENSUS = yarl.URL('https://census.daybreakgames.com')
DBG_STREAMING = yarl.URL('wss://push.planetside2.com/streaming')
DBG_FILES = yarl.URL('https://census.daybreakgames.com/files/ps2/images/static/')

# Nanite Systems
#
# Info: <https://nanite-systems.net/>
NANITE_SYSTEMS = yarl.URL('wss://push.nanite-systems.net/streaming')

# Sanctuary.Census
#
# Info: <https://census.lithafalcon.cc/>
SANCTUARY_CENSUS = yarl.URL('https://census.lithafalcon.cc')


def defaults() -> tuple[yarl.URL, yarl.URL]:
    """Return the default REST and ESS endpoints as a tuple."""
    return DBG_CENSUS, DBG_STREAMING
