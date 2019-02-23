"""ESS (Event Streaming Service) submodule.

The Daybreak Game Company's Census API provides a websocket endpoint
that can be used to retrieve game data in next to real time.

This module contains all the extension code to enable ESS functionality
in the auraxium module. See the repository wiki for details:
https://github.com/leonhard-s/auraxium/wiki
"""

from .client import Client
from .ps2 import *
