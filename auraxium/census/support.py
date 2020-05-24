"""Supporting classes and helper methods for the census module."""

import copy
import enum
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union

CensusValue = Union[float, int, str]
_T = TypeVar('_T')

# This list connects the string literals to the enum values. The index of the
# list element must match the corresponding enum value.
_conversion_list: List[str] = ['', '<', '[', '>', ']', '^', '*', '!']


class CallableAttribute:
    """An attribute wrapper used to chain attribute assignments.

    The setter method is the preferred way to update the attribute. It
    is possible to access and update the value manually through the
    CallableAttribute.value attribute.

    Attributes:
        value: The value of the attribute. This  is the value updated
            by the setter method.

    """

    def __init__(self, setter: Callable[..., _T], default: Any) -> None:
        """Initialise the attribute descriptor.

        This will set up the setter method and default value. It cannot
        set up a reference to the parent object here, this is done in
        the __get__ descriptor method.

        Args:
            setter: The setter method for this attribute.
            default: The default value of the attribute.

        """
        self._default = default
        self._setter = setter
        # NOTE: Due to the decorator being called before the query object is
        # instantiated, we cannot store a reference to the parent object here.
        # We need this reference to make the self attribute behave correctly
        # in the setter method, so it will be set by the __get__ magic method.
        self._last_parent: Optional[_T] = None

    @property
    def value(self) -> Any:
        """Internal property for accessing the per-instance value."""
        return getattr(
            self._last_parent, f'_ca_{self._setter.__name__}', self._default)

    @value.setter
    def value(self, value: Any) -> None:
        setattr(self._last_parent, f'_ca_{self._setter.__name__}', value)

    def __call__(self, *args: Any, **kwargs: Any) -> _T:
        """Call the setter method for this attribute.

        The arguments and return values are identical to the setter.

        Args:
            *args: Positional arguments for the setter.
            **kwargs: Keyword arguments for the setter.

        Returns:
            The return value of the setter method.

        """
        assert self._last_parent is not None, 'Missing reference to parent'
        return self._setter(self._last_parent, *args, **kwargs)

    def __get__(self, instance: Optional[_T],
                owner: Type[_T]) -> 'CallableAttribute':
        """Return the attribute of the owner class or instance.

        This is only used to store a reference to the owner and returns
        a reference to the descriptor itself.

        Args:
            instance: The class instance this attribute was accessed
                through, or None if accessed via the class.
            owner: The owning class of this attribute.

        Returns:
            A reference to the descriptor.
        """
        # NOTE: This sets the "parent" flag whenever this object is accessed,
        # since the descriptor cannot know the parent object at decorator
        # instantiation.
        self._last_parent = instance
        return self


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
    def serialise(enum_value: Union[int, 'SearchModifier']) -> str:
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
            enum_value = enum_value.value
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
            modifier(optional): The search modifier to use. Modifiers
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
        can obscure the actual field value(this is generally not of
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


def query_command(default: Any = None
                  ) -> Callable[[Callable[..., _T]], CallableAttribute]:
    """Turn the given function into a query command.

    This decorator will wrap the given function inside a descriptor,
    effectively creating a callable attribute. Calling this attribute
    will invoke the setter provided to the decorator.

    Note that this will dynamically subclass any object assigned. This
    should mostly be invisible, but it will overwrite any __call__()
    methods defined for that this type.

    Args:
        setter: The setter to invoke when calling the argument.
        default (optional): The default value to initialize the
            attribute to. Defaults to None.

    Returns:
        A descriptor wrapping the given setter function.

    """

    def wrapper(setter: Callable[..., _T]) -> CallableAttribute:
        """Inner wrapper for the query_command decorator.

        The name of the created attribute has the same name as the
        setter function given.

        Args:
            setter: The setter method to use for updating the value.

        Returns:
            A descriptor wrapping the given attribute.

        """
        # Deepcopy used to ensure mutable default values stay distinct between
        # instances
        instance = CallableAttribute(setter, copy.deepcopy(default))
        return instance

    return wrapper
