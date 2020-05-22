"""Low-level Census API wrapper and URL generator.

This module is reponsible for generating the URLs used to interface
with the Census API. It is game agnostic and should work for any game
supporting the Census.

It is mostly intended as an internal helper for the object-oriented
Auraxium interface, but it can also be used by advanced users to
generate their own queries for other use-cases.

This module does not perform any queries; it only generates the URLs.
Use an HTTP library of your choice to perform your queries.
"""

from .query import JoinedQuery, Query, QueryBase
from .support import SearchModifier, SearchTerm
