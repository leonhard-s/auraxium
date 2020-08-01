"""URL generation and validation utility."""

import warnings
from typing import Dict, Iterable, List, Optional, Tuple, Union

import yarl

from .query import JoinedQuery, Query

__all__ = [
    'generate_url',
    'process_join',
]

REST_ENDPOINT = 'https://census.daybreakgames.com'


def generate_url(query: Query, verb: str, validate: bool = True) -> yarl.URL:
    """Generate the URL for a given query.

    This will also recursively process any joined queries.

    Arguments:
        query: The top-level query to process.
        verb: The query verb to use for the query.
        validate (optional): By default, the URL generator will perform
            a number of checks to validate the query, raising errors or
            warnings as necessary. Disabling this flag will skip the
            checks. Defaults to ``True``.

    Returns:
        A yarl URL representing the query.

    """
    # NOTE: The yarl.URL object uses the division operator to chain URI
    # components.

    # Census endpoint
    url = yarl.URL(REST_ENDPOINT)
    # Service ID
    url /= query.service_id
    if validate and query.service_id == 's:example':
        warnings.warn('The default service ID is heavily rate-limited. '
                      'Consider applying for your own service ID at '
                      'https://census.daybreakgames.com/#devSignup')
    # Query verb
    url /= verb
    # Namespace
    url /= query.namespace
    # Collection
    if query.collection is not None:
        url /= query.collection
    elif validate:
        if query.terms:
            warnings.warn(f'No collection specified, but {len(query.terms)} '
                          'query terms provided')
        if query.joins:
            warnings.warn(f'No collection specified, but {len(query.joins)} '
                          'joined queries provided')
    # Top-level query terms
    url = url.with_query([t.as_tuple() for t in query.terms])
    # Process query commands
    url = url.update_query(process_query_commands(query, validate=validate))
    return url


def process_join(join: JoinedQuery, verbose: bool) -> str:
    """Return a string representation of the joined query.

    This generates is the string that will be inserted into the
    URL. This will also recursively process any inner joins added.

    Arguments:
        verbose(optional): By default, the serialisation will try
            to save space by omitting fields left at their default
            value. Set this flag to True to change that. Defaults
            to ``False``.

    Returns:
        The string representation of the joined query.

    """
    # The collection (sometimes referred to as "type" in the docs) to join
    string = 'type:' if verbose else ''
    string += str(join.collection)
    # The fields used to link the two collections
    if join.parent_field is not None:
        string += f'^on:{join.parent_field}'
    if join.child_field is not None:
        string += f'^to:{join.child_field}'
    # Flags
    if join.is_list or verbose:
        string += '^list:' + ('1' if join.is_list else '0')
    if not join.is_outer or verbose:
        string += '^outer:' + ('1' if join.is_outer else '0')
    # Show/hide field lists
    if join.commands['show']:
        string += '^show:' + '\''.join(str(s) for s in join.commands['show'])
    elif join.commands['hide']:
        string += '^hide:' + '\''.join(str(s) for s in join.commands['hide'])
    # Inject at name
    if join.inject_at is not None:
        string += f'^inject_at:{join.inject_at}'
    # QueryBase terms
    if join.terms:
        string += '^terms:' + '\''.join(t.serialise() for t in join.terms)
    # Process nested (inner) joins
    if join.joins:
        string += '('
        string += ','.join(j.serialise(verbose) for j in join.joins)
        string += ')'
    return string


def process_query_commands(query: Query,
                           validate: bool = True) -> Dict[str, str]:
    """Process any query commands defined for the given query.

    This also recursively processes any joins defined.

    Arguments:
        query: The top-level query to process.
        validate (optional): Whether to perform checks on the query and
            warn the user about bad arguments. Defaults to ``True``.

    Returns:
        A dict of all query commands for the given query, this will be
        an empty dict if the query does not use any query commands.

    """
    commands: Dict[str, str] = {}
    # c:show
    if query.commands['show']:
        commands['show'] = ','.join(str(f) for f in query.commands['show'])
        if validate and query.commands['hide']:
            warnings.warn('Query.show and Query.hide are mutually exclusive, '
                          'the latter will be ignored')
    # c:hide
    elif query.commands['hide']:
        commands['hide'] = ','.join(str(f) for f in query.commands['hide'])
    # c:sort
    if query.commands['sort']:
        commands['sort'] = ','.join(_process_sorts(query.commands['sort']))
    # c:has
    if query.commands['has']:
        commands['has'] = ','.join(query.commands['has'])
    # c:resolve
    if query.commands['resolve']:
        commands['resolve'] = ','.join(query.commands['resolve'])
    # c:case
    if not query.commands['case']:
        commands['case'] = '0'
    # c:limit
    if query.commands['limit'] > 1:
        commands['limit'] = str(query.commands['limit'])
        if validate and query.commands['limit_per_db'] > 1:
            warnings.warn('Query.limit and Query.limit_per_db are mutually '
                          'exclusive, the latter will be ignored')
    # c:limitPerDB
    elif query.commands['limit_per_db'] > 1:
        commands['limitPerDB'] = str(query.commands['limit_per_db'])
    # c:start
    if query.commands['start'] > 0:
        commands['start'] = str(query.commands['start'])
    # c:includeNull
    if query.commands['include_null']:
        commands['includeNull'] = '1'
    # c:lang
    if query.commands['lang'] is not None:
        commands['lang'] = query.commands['lang']
    # c:join
    if query.joins:
        commands['join'] = ','.join(j.serialise() for j in query.joins)
    # c:tree
    if query.commands['tree'] is not None:
        commands['tree'] = _process_tree(query.commands['tree'])
    # c:timing
    if query.commands['timing']:
        commands['timing'] = '1'
    # c:exactMatchFirst
    if query.commands['exact_match_first']:
        commands['exactMatchFirst'] = '1'
    # c:distinct
    if query.commands['distinct'] is not None:
        commands['distinct'] = query.commands['distinct']
    # c:retry
    if not query.commands['retry']:
        commands['retry'] = '0'
    # Add the 'c:' prefix to all of the keys
    commands = {f'c:{k}': v for k, v in commands.items()}
    return commands


def _process_sorts(sorts: Iterable[Union[str, Tuple[str, bool]]]) -> List[str]:
    """Process a top-level query's sort_by attribute into a list.

    This mostly handles the sorting direction tuples.

    Arguments:
        sorts: The sorting values to process.

    Raises:
        ValueError: Raised if an invalid sorting key is encountered.

    Returns:
        A list of sorting fields with sort order tokens.

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
    """Process the dict created by the :meth:`Query.as_tree()` method.

    Arguments:
        tree: The mapping to process.

    Returns:
        The string representation of the tree command.

    """
    string = str(tree['field'])
    if tree['prefix']:
        string += f'^prefix:{tree["prefix"]}'
    if tree['is_list']:
        string += '^list:1'
    if tree['start'] is not None:
        string += f'^start{tree["start"]}'
    return string
