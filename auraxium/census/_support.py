"""Supporting classes and helper methods for the census module."""

import dataclasses
import enum
from typing import Any, TypeVar

__all__ = [
    'CensusValue',
    'JoinedQueryData',
    'QueryBaseData',
    'QueryData',
    'SearchModifier',
    'SearchTerm'
]

# This list connects the string literals to the enum values. The index of the
# list element must match the corresponding enum value.
_MODIFIER_LITERALS: list[str] = ['', '<', '[', '>', ']', '^', '*', '!']

CensusValue = float | int | str
_QueryBaseDataT = TypeVar('_QueryBaseDataT', bound='QueryBaseData')


class SearchModifier(enum.Enum):
    """Enumerates the search modifiers available for Term objects.

    Note that a given search modifier may not be valid for all fields.

    The following is a list of all search modifier literals and their
    corresponding enum value:::

       EQUAL_TO: '',               LESS_THAN: '<',
       LESS_THAN_OR_EQUAL: '[',    GREATER_THAN: '>',
       GREATER_THAN_OR_EQUAL: ']', STARTS_WITH: '^',
       CONTAINS: '*',              NOT_EQUAL: '!'
    """

    EQUAL_TO = 0
    LESS_THAN = 1
    LESS_THAN_OR_EQUAL = 2
    GREATER_THAN = 3
    GREATER_THAN_OR_EQUAL = 4
    STARTS_WITH = 5
    CONTAINS = 6
    NOT_EQUAL = 7

    EQ = EQUAL_TO
    """Alias for :class:`EQUAL_TO <SearchModifier>`.

    .. versionadded:: 0.2
    """

    LT = LESS_THAN
    """Alias for :class:`LESS_THAN <SearchModifier>`.

    .. versionadded:: 0.2
    """

    LTE = LESS_THAN_OR_EQUAL
    """Alias for :class:`LESS_THAN_OR_EQUAL <SearchModifier>`.

    .. versionadded:: 0.2
    """

    GT = GREATER_THAN
    """Alias for :class:`GREATER_THAN <SearchModifier>`.

    .. versionadded:: 0.2
    """

    GTE = GREATER_THAN_OR_EQUAL
    """Alias for :class:`GREATER_THAN_OR_EQUAL <SearchModifier>`.

    .. versionadded:: 0.2
    """

    SW = STARTS_WITH
    """Alias for :class:`STARTS_WITH <SearchModifier>`.

    .. versionadded:: 0.2
    """

    IN = CONTAINS
    """Alias for :class:`CONTAINS <SearchModifier>`.

    .. versionadded:: 0.2
    """

    NE = NOT_EQUAL
    """Alias for :class:`NOT_EQUAL <SearchModifier>`.

    .. versionadded:: 0.2
    """

    @classmethod
    def from_value(cls, value: CensusValue) -> 'SearchModifier':
        """Infer the search modifier from a given value.

        If the input is a string, its first character will be compared
        against the corresponding API literals. If a match is found,
        the corresponding SearchModifier enum value is returned.

        If the input is not a string or its first character does not
        match any API literal, this will return
        :class:`SearchModifier.EQUAL_TO <SearchModifier>`.

        :param value: A value to infer the search modifier from.
        :type value: float | int | str
        :raises ValueError: Raised if `value` is an empty string.
        :return: The search modifier for the value provided.
        """
        if not isinstance(value, str):
            return cls(cls.EQUAL_TO)
        if not value:
            raise ValueError('Value may not be an empty string')
        try:
            return cls(_MODIFIER_LITERALS.index(value[0]))
        except ValueError:
            return cls(cls.EQUAL_TO)

    @staticmethod
    def serialise(enum_value: 'int | SearchModifier') -> str:
        """Return the string literal for the given enum value.

        This is primarily used during URL generation.

        :param enum_value: The enum value or index to serialise.
        :type enum_value: int | SearchModifier
        :raises ValueError: Raised if the provided integer exceeds the
           value range of the enum.
        :return: The string representation of the search modifier. This
           will be an empty string for
           :class:`SearchModifier.EQUAL_TO <SearchModifier>`.
        """
        if isinstance(enum_value, SearchModifier):
            enum_value = enum_value.value
        assert isinstance(enum_value, int)
        try:
            return _MODIFIER_LITERALS[enum_value]
        except IndexError as err:
            raise ValueError(f'Invalid enum value {enum_value}') from err


class SearchTerm:
    """A query filter term.

    Search terms are key-value pairs with an optional search modifier
    determining how these values will be compared. See the
    :class:`SearchModifier` enum for details on the available search
    modifiers.

    .. attribute:: field
       :type: str

       The field to filter by.

    .. attribute:: value
       :type: float | int | str

       The value to compare the field against.

    .. attribute:: modifier
       :type: SearchModifier

       The :class:`SearchModifier` to use.
    """

    def __init__(self, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO) -> None:
        """Initialise a new search term.

        Search terms are used to filter the results before returning.
        This is particularly important for lists returned by
        :class:`JoinedQuery` instnaces as they do not have access to
        limiting mechanisms like :class:`Query`, easily resulting in
        excessively long return lists.

        Use the :meth:`SearchTerm.infer` factory if you prefer defining
        search modifiers via their string literals as used by the API,
        rather than manually specifying the enum value.

        :param str field: The field to compare.
        :param value: The value to compare the field against.
        :type value: float | int | str
        :param SearchModifier modifier: The search modifier to use.
           Modifiers can be used to get non-exact or partial matches.
        """
        self.field: str = field
        self.value: CensusValue = value
        self.modifier: SearchModifier = modifier

    def as_tuple(self) -> tuple[str, str]:
        """Return a key/value pair representing the search term.

        This is a helper function that calls
        :meth:`SearchTerm.serialise` and then splits the returned
        string at the equal sign.

        :return: A key/value pair representing teh search term.
        """
        key, value = self.serialise().split('=', 1)
        return key, value

    @classmethod
    def infer(cls, field: str, value: CensusValue) -> 'SearchTerm':
        """Infer a term from the given field and value.

        This is a more natural way of defining search terms for users
        familiar with the API literals. See the docstring of the
        :class:`SearchModifier` enumerator for a list of search
        modifiers.

        Note that this requires the value to be a str instance; this
        can obscure the actual field value (this is generally not of
        concern as this information will be lost during URL generation
        regardless).

        :param str field: The field to compare.
        :param value: The value to compare the field against. If
           `value` is a subclass of :class:`str`, its first character
           will be checked for search modifier literals.
        :type value: float | int | str
        :return: A new :class:`SearchTerm` with a pre-defined
           :class:`SearchModifier`.
        """
        term = cls(field=field, value=value)
        term.modifier = SearchModifier.from_value(value)
        # If a search modifier other than EQUAL_TO was returned, the
        # SearchModifier.from_value() function has found a literal in the
        # string.
        # This must now be cut from the value string.
        if term.modifier != SearchModifier.EQUAL_TO:
            assert isinstance(value, str)
            term.value = value[1:]
        return term

    def serialise(self) -> str:
        """Return the literal representation of the search term.

        This is the string that will added to the URL's query string as
        part of the URL generator.

        :return: The string representation of the search term.
        """
        return (f'{self.field}={SearchModifier.serialise(self.modifier)}'
                f'{self.value}')


@dataclasses.dataclass()
class QueryBaseData:
    """A dataclass used to store generic query information.

    Refer to the corresponding setter methods for details.
    """

    collection: str | None

    # Redundant annotation is required to appease both pyright/pylance
    # and the dataclass runtime checks, see
    # https://github.com/microsoft/pyright/issues/10277
    hide: list[str] = (
        dataclasses.field(default_factory=list[str]))
    joins: list['JoinedQueryData'] = (
        dataclasses.field(default_factory=list['JoinedQueryData']))
    show: list[str] = (
        dataclasses.field(default_factory=list[str]))
    terms: list[SearchTerm] = (
        dataclasses.field(default_factory=list[SearchTerm]))

    @classmethod
    def from_base(cls: type[_QueryBaseDataT],
                  data: 'QueryBaseData') -> _QueryBaseDataT:
        """Helper used to copy the base query data components."""
        return cls(**data.__dict__)


@dataclasses.dataclass()
class QueryData(QueryBaseData):
    """A dataclass used to store global flags and settings for queries.

    Refer to the corresponding setter methods for details.
    """
    # pylint: disable=too-many-instance-attributes

    case: bool = True
    distinct: str | None = None
    exact_match_first: bool = False
    has: list[str] = dataclasses.field(default_factory=list[str])
    include_null: bool = False
    lang: str | None = None
    limit: int = 1
    limit_per_db: int = 1
    namespace: str = 'ps2:v2'
    resolve: list[str] = dataclasses.field(default_factory=list[str])
    retry: bool = True
    service_id: str = 's:example'
    sort: list[str | tuple[str, bool]] = (
        dataclasses.field(default_factory=list[str | tuple[str, bool]]))
    start: int = 0
    timing: bool = False
    tree: dict[str, Any] | None = None


@dataclasses.dataclass()
class JoinedQueryData(QueryBaseData):
    """Data class for joined queries in the API.

    Refer to the corresponding setter methods for details.
    """

    inject_at: str | None = None
    is_list: bool = False
    is_outer: bool = True
    field_on: str | None = None
    field_to: str | None = None
