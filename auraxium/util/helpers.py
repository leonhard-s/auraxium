from ..census import Query
from ..ps2 import (Achievement, Character, Currency, Directive, DirectiveTier,
                   DirectiveTree, DirectiveTreeCategory, Faction, Item,
                   Outfit, Region, Skill, SkillCategory, SkillLine,
                   Title, Vehicle, Zone)


def get_by_name(datatype, name, ignore_case=False, locale=None):

    field_name = 'name'

    # The `character` collection has the redundant subkey 'first'
    if datatype == Character:
        field_name += '.first'

    # If a locale has been specified, append the locale subkey
    if locale is not None:
        field_name += '.' + locale

    # If case is to be ignored
    if ignore_case:
        if datatype in [Character, Outfit]:
            # Use the lowercase version of the field
            field_name += '_lower'
            q = Query(type=datatype._collection)
            q.add_filter(field=field_name, value=name.lower())
        else:
            # There is no lowercase field, use the case-insensitive search
            q = Query(type=datatype._collection, check_case=False)
            q.add_filter(field=field_name, value=name)
    else:
        q = Query(type=datatype._collection).add_filter(
            field=field_name, value=name)

    data = q.get_single()

    datatype(id=data[datatype._collection + '_id'])
    datatype._populate(data_override=data)
    return datatype


def name_to_id(datatype, name, check_case=False):
    """Retrieves the id of a given object by its name.

    This only works with exact matches.

    Parameters
    ----------
    datatype
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

    localized_collections = [Achievement, Character, Currency,
                             Directive, DirectiveTier, DirectiveTree,
                             DirectiveTreeCategory, Faction, Item, Region,
                             Skill, SkillCategory, SkillLine, Title,
                             Vehicle, Zone]

    q = Query(datatype._collection)
    q.show('{}_id'.format(datatype._collection))

    # Special case: character names
    if datatype == Character:
        _ = q.add_filter('name.first', name) if check_case else q.add_filter(
            'name.first_lower', name.lower())

    elif datatype in localized_collections:
        # Apply the filter term
        q.add_filter('name.en', name)

    else:
        print('WARNING')

    data = q._retrieve('get')['{}_list'.format(datatype._collection)][0]

    return int(data['{}_id'.format(datatype._collection)])


def prune_dict(input_dict):
    """Returns a copy of the dictionary without None values.

    Returns a copy of the input dictionary that only contains keys that are not
    equal to None.

    """

    output_dict = {}
    for k in input_dict.keys():
        if input_dict[k] is not None and input_dict[k] != 'NULL':
            output_dict[k] = input_dict[k]
        # Recursively prune any inner dictionaries
        elif isinstance(input_dict[k], dict):
            output_dict[k] = prune_dict(input_dict[k].copy())
    return output_dict
