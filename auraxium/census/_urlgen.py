"""URL generation and validation utility."""

import warnings
from typing import Dict, Iterable, List, Optional, Tuple, Union

import yarl

from ..endpoints import defaults as default_endpoints
from ._support import JoinedQueryData, QueryData

__all__ = [
    'generate_url',
    'process_join',
]


def generate_url(query: QueryData, verb: str, validate: bool = True,
                 endpoint: Optional[yarl.URL] = None) -> yarl.URL:
    """Generate the URL for a given query.

    This will also recursively process any joined queries.

    :param QueryData query: The top level query to process.
    :param str verb: The query verb to use for the query.
    :param bool validate: By default, the URL generator will perform a
       number of checks to validate the query, raising errors or
       warnings as necessary. Disabling this flag will skip these
       checks.
    :param endpoint: The API endpoint to use. Allows use of community
       APIs using the same syntax as the official API. If not set, will
       default to the official API endpoint.
    :type endpoint: :class:`yarl.URL` | :obj:`None`
    :return: A :class:`yarl.URL` representing the query.
    """
    # NOTE: The yarl.URL object uses the division operator to chain URI
    # components.

    # Census endpoint
    default = default_endpoints()[0]
    url = yarl.URL(endpoint or default)
    # Service ID
    if url == default:
        url /= query.service_id
    if validate and endpoint == default and query.service_id == 's:example':
        warnings.warn('The default service ID is heavily rate-limited. '
                      'Consider applying for your own service ID at '
                      'https://census.daybreakgames.com/#devSignup')
    # Query verb
    url /= verb
    # Namespace
    url /= query.namespace
    # Collection
    if (collection := query.collection) is not None:
        url /= collection
    elif validate:
        if query.terms:
            warnings.warn(f'No collection specified, but {len(query.terms)} '
                          'query terms provided')
        elif query.joins:
            warnings.warn(f'No collection specified, but {len(query.joins)} '
                          'joined queries provided')
    # Top-level query terms
    url = url.with_query([t.as_tuple() for t in query.terms])
    # Process query commands
    url = url.update_query(_process_query_commands(query, validate=validate))
    return url


def process_join(data: JoinedQueryData, verbose: bool) -> str:
    """Return a string representation of the joined query.

    This generates is the string that will be inserted into the
    URL. This will also recursively process any inner joins added.

    :param JoinedQueryData data: The data representing the joined
       query.
    :param bool verbose: By default, the serialisation will try to save
       space by omitting fields left at their default value. Set this
       flag to instead always write all values. This is primarily a
       troubleshooting option.
    :return: The string representation of the joined query.
    """
    # The collection (sometimes referred to as "type" in the docs) to join
    string = 'type:' if verbose else ''
    string += str(data.collection)
    # The fields used to link the two collections
    if (parent := data.field_on) is not None:
        string += f'^on:{parent}'
    if (child := data.field_to) is not None:
        string += f'^to:{child}'
    # Flags
    if (is_list := data.is_list) or verbose:
        string += '^list:' + ('1' if is_list else '0')
    if not (is_outer := data.is_outer) or verbose:
        string += '^outer:' + ('1' if is_outer else '0')
    # Show/hide field lists
    if show := data.show:
        string += '^show:' + '\''.join(str(s) for s in show)
    elif hide := data.hide:
        string += '^hide:' + '\''.join(str(s) for s in hide)
    # Inject at name
    if (name := data.inject_at) is not None:
        string += f'^inject_at:{name}'
    # QueryBase terms
    if terms := data.terms:
        string += '^terms:' + '\''.join(t.serialise() for t in terms)
    # Process nested (inner) joins
    if joins := data.joins:
        string += f'({",".join(process_join(j, verbose) for j in joins)})'
    return string


def _process_query_commands(data: QueryData,
                            validate: bool = True) -> Dict[str, str]:
    """Process any query commands defined for the given query.

    This also recursively processes any joins defined.

    :param QueryData data: The top level query to process.
    :param bool validate: Whether to perform checks on the query and
       warn the user about bad arguments.
    :return: A dict of all query commands for the given query, this
       will be an empty dict if the query does not use any query
       commands.
    """
    commands: Dict[str, str] = {}
    # c:show
    if show := data.show:
        commands['show'] = ','.join(str(f) for f in show)
        if validate and data.hide:
            warnings.warn('Query.show and Query.hide are mutually exclusive, '
                          'the latter will be ignored')
    # c:hide
    elif hide := data.hide:
        commands['hide'] = ','.join(str(f) for f in hide)
    # c:sort
    if sort := data.sort:
        commands['sort'] = ','.join(_process_sorts(sort))
    # c:has
    if has := data.has:
        commands['has'] = ','.join(has)
    # c:resolve
    if resolve := data.resolve:
        commands['resolve'] = ','.join(resolve)
    # c:case
    if not data.case:
        commands['case'] = '0'
    # c:limit
    if (limit := data.limit) > 1:
        commands['limit'] = str(limit)
        if validate and data.limit_per_db > 1:
            warnings.warn('Query.limit and Query.limit_per_db are mutually '
                          'exclusive, the latter will be ignored')
    # c:limitPerDB
    elif (limit_per_db := data.limit_per_db) > 1:
        commands['limitPerDB'] = str(limit_per_db)
    # c:start
    if (start := data.start) > 0:
        commands['start'] = str(start)
    # c:includeNull
    if data.include_null:
        commands['includeNull'] = '1'
    # c:lang
    if (lang := data.lang) is not None:
        commands['lang'] = lang
    # c:join
    if data.joins:
        commands['join'] = ','.join(
            process_join(j, False) for j in data.joins)
    # c:tree
    if (tree := data.tree) is not None:
        commands['tree'] = _process_tree(tree)
    # c:timing
    if data.timing:
        commands['timing'] = '1'
    # c:exactMatchFirst
    if data.exact_match_first:
        commands['exactMatchFirst'] = '1'
    # c:distinct
    if (distinct := data.distinct) is not None:
        commands['distinct'] = distinct
    # c:retry
    if not data.retry:
        commands['retry'] = '0'
    # Add the 'c:' prefix to all of the keys
    commands = {f'c:{k}': v for k, v in commands.items()}
    return commands


def _process_sorts(sorts: Iterable[Union[str, Tuple[str, bool]]]) -> List[str]:
    """Process a top-level query's sort_by attribute into a list.

    This mostly handles the sorting direction tuples.

    :param sorts: The sorting values to process.
    :type sorts: collections.abc.Iterable[str or tuple[str,bool]]
    :raises ValueError: Raised if an invalid sorting key is
       encountered.
    :return: A list of sorting fields with sort order tokens.
    """
    processed: List[str] = []
    for sort in sorts:
        # Plain strings can be kept as-is
        if isinstance(sort, str):
            processed.append(sort)
        # Non-string objects are expected to be tuples showing sort order
        else:
            try:
                field, sort_order = sort
            except ValueError as err:
                raise ValueError(f'Invalid sort key: {sort}') from err
            processed.append(field if sort_order else f'{field}:-1')
    return processed


def _process_tree(tree: Dict[str, Optional[Union[str, bool]]]) -> str:
    """Process the dict created by the :meth:`Query.as_tree` method.

    :param tree: The dictionary to process.
    :type tree: dict[str, str or bool or None]
    :return: The string representation of the tree.
    """
    string = str(tree['field'])
    if prefix := tree['prefix']:
        string += f'^prefix:{prefix}'
    if tree['is_list']:
        string += '^list:1'
    if (start := tree['start']) is not None:
        string += f'^start:{start}'
    return string
