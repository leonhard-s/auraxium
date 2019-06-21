"""The auraxium wrapper module for the DBG census API.

For usage instructions and additional information, visit
https://github.com/leonhard-s/auraxium/.
"""

from .census import SearchModifier
from .query import Query
from .ess import Client

namespace = 'ps2:v2'
service_id = 'example'
