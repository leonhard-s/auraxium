"""ABC definition for the reports interface."""

import abc
from typing import Dict, List, Sequence, Type, TypeVar

from ..base import Ps2Object
from ..types import CensusData

_ReportT = TypeVar('_ReportT', bound='Report')
_ObjOrIntT = TypeVar('_ObjOrIntT', Ps2Object, int)


class Report(metaclass=abc.ABCMeta):
    """The abstract base class used for report classes.

    Reports are used to efficiently run complex queries for multiple
    objects without having to loop over them.
    This allows bundling similar queries together, greatly reducing the
    number of API calls required to retrieve the wanted data.

    Subclasses must implement a ``Report.generate()`` method as the
    factory method to create report instances for given inputs. For
    typing and inheritance reasons, no such method is implemented by
    default.

    Additionally, they must implement the ``Report.from_census()``
    method to process the data they returned and convert it into a
    properly typed instance of themselves.

    The following is an example for what a ``Report.generate()`` method
    should look like. Keep in mind that subclasses are free to update
    the argument types or add additional keyword arguments as needed.

    .. code-block:: python3

        @classmethod
        async def generate(
                cls: Type[ReportT], *args: T,
                client: Client) -> Dict[T, ReportT]:
            # Step 1: Retrieve a series of integers that can be passed
            # to a query
            obj_ids = cls.get_ids(args)
            # Step 2: Run as many queries as required to generate the
            # reports
            data: Dict[int, ReportT] = {}
            ...
            # Step 3: Return a dictionary mapping the input positional
            # arguments to their reports
            return cls.match_reports(data, args)

    Use of the helper methods :meth:`get_ids()` and
    :meth:`match_reports()` method is optional, but does help with
    creating :class:`Ps2Object`-compatible report factories.

    Refer to the built-in reports found in the :mod:`auraxium.reports`
    namespace for additional examples.

    """

    @classmethod
    @abc.abstractmethod
    def from_census(cls: Type[_ReportT], data: CensusData) -> _ReportT:
        """Generate a report instance from the given census data.

        This will be generally called for every instance retrieved via
        the :meth:`Report.generate()` method. The contents of the data
        dictionary passed depends on the custom query used.

        Arguments:
            data: The census dictionary to process.

        Returns:
            A report instance matching the payload provided.

        """
        ...

    @staticmethod
    def get_ids(arguments: Sequence[_ObjOrIntT]) -> List[int]:
        """Extract the IDs from a given sequence of input arguments.

        This expects the input types to be either integers or objects
        with an integer as their ``.id`` attribute.

        Arguments:
            arguments: The given sequence of input types.

        Returns:
            A list of integers representing the input arguments.

        """
        return [i if isinstance(i, int) else i.id  # type: ignore
                for i in arguments]

    @staticmethod
    def match_reports(reports: Dict[int, _ReportT],
                      arguments: Sequence[_ObjOrIntT]
                      ) -> Dict[_ObjOrIntT, _ReportT]:
        """Group a dictionary of ID-specific reports.

        The ``Report.generate()`` class is expected to return a
        dictionary mapping its positional input arguments to the
        reports generated for them.

        This method will convert a dictionary mapping the object IDs to
        their reports into one mapping the original arguments to the
        reports.

        Arguments:
            reports: A mapping of unique IDs to reports generated for
                them.
            arguments: A sequence of types that will be used as the new
                keys for the returned dictionary. This may be integer
                subclasses or classes featuring an integer in their
                ``.id`` attribute.

        Returns:
            A mapping of input arguments to the report instance
            matching their ID.

        """
        grouped: Dict[_ObjOrIntT, _ReportT] = {}
        for arg in arguments:
            key = arg if isinstance(arg, int) else arg.id
            grouped[arg] = reports[key]  # type: ignore
        return grouped
