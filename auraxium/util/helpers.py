from ..census import Query
from ..planetside import Character


def name_to_id(data_type, name, check_case=False):
    """Retrieves the id of a given object by its name.

    This only works with exact matches.

    Parameters
    ----------
    data_type
        The data type to search for the name specified
    name : str
        The name of the entry to retrieve. Must be an exact.
    check_case : Boolean
        Whether to check for case when looking up the name. Defaults to False.

    Returns
    -------
    int
        The unique ID of the entry.

    """

    q = Query(data_type)
    q.show('{}_id'.format(data_type._collection))

    # Special case: character names
    if data_type == Character:
        q.add_filter('name.first', name) if check_case else q.add_filter(
            'name.first_lower', name.lower())

    else:
        # Apply the filter term
        q.add_filter('name', name) if check_case else q.add_filter(
            'name_lower', name.lower())

    data = q._retrieve('get')['{}_list'.format(data_type._collection)][0]

    return int(data['{}_id'.format(data_type._collection)])
