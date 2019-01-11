from ..census import Query
from ..ps2 import (Achievement, AlertType, Character, Currency, Directive,
                   DirectiveTier, DirectiveTree, DirectiveTreeCategory,
                   Faction, Item, Region, Skill, SkillCategory, SkillLine,
                   SkillSet, Title, Vehicle, Zone)


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

    localized_collections = [Achievement, AlertType, Character, Currency,
                             Directive, DirectiveTier, DirectiveTree,
                             DirectiveTreeCategory, Faction, Item, Region,
                             Skill, SkillCategory, SkillLine, SkillSet, Title,
                             Vehicle, Zone]

    q = Query(data_type._collection)
    q.show('{}_id'.format(data_type._collection))

    # Special case: character names
    if data_type == Character:
        q.add_filter('name.first', name) if check_case else q.add_filter(
            'name.first_lower', name.lower())

    elif data_type in localized_collections:
        # Apply the filter term
        q.add_filter('name.en', name)

    else:
        print('WARNING')

    data = q._retrieve('get')['{}_list'.format(data_type._collection)][0]

    return int(data['{}_id'.format(data_type._collection)])


def prune_dict(input_dict):
    """Returns a copy of the dictionary without None values.

    Returns a copy of the input dictionary that only contains keys that are not
    equal to None.

    """

    output_dict = {}
    for k in input_dict.keys():
        if input_dict[k] != None and input_dict[k] != 'NULL':
            output_dict[k] = input_dict[k]
        # Recursively prune any inner dictionaries
        elif isinstance(input_dict[k], dict):
            output_dict[k] = prune_dict(input_dict[k].copy())
    return output_dict
