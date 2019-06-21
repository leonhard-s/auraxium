from typing import Tuple
from .census import List, Term
from .log import logger
from .type import CensusValue


class Join():
    """Represents an inner (or joined) query.

    Created by the `Query.join()` and `Join.join()` methods.
    Do not instantiate manually.
    """

    def __init__(self, collection: str, inject_at: str = '',
                 is_list: bool = False,  on: str = '', is_outer: bool = True,
                 to: str = '', **kwargs: CensusValue) -> None:
        """Initializer."""
        self.collection = collection
        self.hide: List[str] = []
        self._inner_joins: List['Join'] = []
        self.is_list = is_list
        self.is_outer = is_outer
        self.inject_at = inject_at
        self.parent_field = on
        self.child_field = to
        self.show: List[str] = []
        # Additional kwargs are passed on to the `add_term` method
        self._terms: List[Term] = []
        _ = [Term(k.replace('__', '.'), kwargs[k]) for k in kwargs.keys()]

    def hide(self, *args: str) -> 'Join':
        """Hide the given field names from the response."""
        self.hide = list(args)
        if self.hide and self.show:
            logger.warning('"Show" will take precedent over "hide".')
        return self

    def join(self, collection: str, inject_at: str = '',
             is_list: bool = False, on: str = '', is_outer: bool = True,
             to: str = '', **kwargs: Tuple[str, CensusValue]) -> 'Join':
        """Create an inner join for this join.

        All arguments passed to this function are forwarded to the new
        Join's initializer. The created join is returned.
        """
        inner_join = Join(collection, inject_at, is_list,
                          on, is_outer, to, **kwargs)
        self._inner_joins.append(inner_join)
        return inner_join

    def show(self, *args: str) -> 'Join':
        """Only include the given field names in the response."""
        self.show = list(args)
        if self.hide and self.show:
            logger.warning('"Show" will take precedent over "hide".')
        return self

    def terms(self, *args: Term) -> 'Join':
        """Apply the given list of terms to the join."""
        self._terms = list(args)
        return self

    def process_join(self) -> str:
        """Process the join and return its string representation.

        This also recursively processes any inner joins.
        """
        # The collection (sometimes referred to a "type" in the docs) of the join
        string = self.collection
        # Keys
        if self.is_list:
            string += '^list:1'
        if not self.is_outer:
            string += '^outer:0'
        if self.inject_at:
            string += '^inject_at:' + self.inject_at
        if self.parent_field:
            string += '^on:' + self.parent_field
        if self.child_field:
            string += '^to:' + self.child_field
        # Show & hide
        if self.show:
            string += '^show:' + ','.join(self.show)
            if self.hide:
                logger.warning('"c:show" overwrites "c:hide"')
        elif self.hide:
            string += '^hide:' + ','.join(self.hide)
        # Terms
        if self._terms:
            string += '^terms:' + '\''.join([t.to_url() for t in self._terms])
        # Process inner joins
        string += ''.join(['(' + j.process_join() +
                           ')' for j in self._inner_joins])
        return string
