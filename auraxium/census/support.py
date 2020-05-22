"""Supporting classes and helper methods for the census module."""

import enum
from typing import List, Tuple, Union

CensusValue = Union[float, int, str]

# This list connects the string literals to the enum values. The index of the
# list element must match the corresponding enum value.
_conversion_list: List[str] = ['', '<', '[', '>', ']', '^', '*', '!']


class SearchModifier(enum.Enum):
    """Enumerates the search modifiers available for Term objects.

    Note that a given search modifier may not be valid for all fields.

    The following is a list of all search modifier literals and their
    corresponding enum value:

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

    @classmethod
    def from_value(cls, value: CensusValue) -> 'SearchModifier':
        """Infer the search modifier from a given value.

        If the input is a string, its first character will be compared
        against the corresponding API literals. If a match is found,
        the corresponding SearchModifier enum value is returned.

        If the input is not a string or its first character does not
        match any API literal, this will return EQUAL_TO.

        Args:
            value: A value to infer the search modifier from.

        Returns:
            The search modifier for the value provided.

        """
        # Return EQUAL_TO for non-string values
        if not isinstance(value, str):
            return cls(cls.EQUAL_TO)
        # For strings, return the corresponding enum value
        try:
            return cls(_conversion_list.index(value[0]))
        except ValueError:
            return cls(cls.EQUAL_TO)

    @staticmethod
    def serialise(enum_value: Union[int, SearchModifier]) -> str:
        """Return the string literal for the given enum value.

        This is mostly used during URL generation.

        Args:
            enum_value: The enum value or index to serialise.

        Raises:
            ValueError: Raised if the provided integer exceeds the
                value range of the enum.

        Returns:
            The string representation of the search modifier. This will
            be an empty string for SearchModifier.EQUAL_TO.

        """
        # Convert the enum value to an integer
        if isinstance(enum_value, SearchModifier):
            enum_value = SearchModifier.value
        assert isinstance(enum_value, int)
        # Return the appropriate string literal
        try:
            return _conversion_list[enum_value]
        except IndexError as err:
            raise ValueError(f'Invalid enum value {enum_value}') from err


class SearchTerm:
    """Represents a single query term."""

    def __init__(self, field: str, value: CensusValue,
                 modifier: SearchModifier = SearchModifier.EQUAL_TO) -> None:
        """Initialise a new search term.

        Search terms are used to filter the results before returning.
        This is particularly important for lists returned by joined
        queries, as they do not have access to limiting mechanisms like
        Query, easily resulgint in excessively long return lists.

        Use the SearchTerm.infer() factory if you prefer defining
        search modifiers via their string literals as used by the API,
        rather than manually specifying the enum value.

        Args:
            field: The field to compare.
            value: The value to compare the field against.
            modifier (optional): The search modifier to use. Modifiers
                can be used to get non-exact or partial matches.
                Defaults to SearchModifier.EQUAL_TO.

        """
        self.field = field
        self.value = value
        self.modifier = modifier

    def as_tuple(self) -> Tuple[str, str]:
        """Return a key/value pair representing the search term.

        This is a helper function that calls SearchTerm.serialise() and
        then splits the returned string at the equal sign.

        Returns:
            A key/value pair representing the search term.

        """
        key, value = self.serialise().split('=', 1)
        return key, value

    @classmethod
    def infer(cls, field: str, value: CensusValue) -> 'SearchTerm':
        """Infer a term from the given field and value.

        This is a more natural way of defining search terms for users
        familiar with the API literals. See the docstring of the
        SearchModifier enum for a list of search modifiers.

        Note that this requires the value to be a str instance; this
        can obscure the actual field value (this is generally not of
        concern as this information will be lost during URL generation
        regardless).

        Args:
            field: The field to compare.
            value: The value to compare the field against. If a string,
                it will be checked for a search modifier literal.

        Returns:
            A new SearchTerm with a pre-defined search modifier.

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

        Returns:
            The string representation of the search term.

        """
        literal = f'{self.field}='
        literal += SearchModifier.serialise(self.modifier)
        literal += str(self.value)
        return literal
