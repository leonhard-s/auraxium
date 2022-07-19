"""Third-party community endpoints compatible with Auraxium."""

from typing import Tuple
import yarl

# Daybreak Game Company Census API
#
# Info: <http://census.daybreakgames.com/>
DBG_CENSUS = yarl.URL('https://census.daybreakgames.com')
DBG_STREAMING = yarl.URL('wss://push.planetside2.com/streaming')
DBG_FILES = yarl.URL(
    'https://census.daybreakgames.com/files/ps2/images/static/')


def defaults() -> Tuple[yarl.URL, yarl.URL]:
    """Return the default REST and ESS endpoints as a tuple."""
    return DBG_CENSUS, DBG_STREAMING
