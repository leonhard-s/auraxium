"""Custom data type definitions. Temporary."""

from typing import NamedTuple, Union

Term = NamedTuple('Term', [('field', str), ('value', Union[str, int, float])])
