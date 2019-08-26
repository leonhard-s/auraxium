"""Helper methods and shortcuts for common Auraxium."""

from typing import Optional
from ..query import Query


def name_from_id(collection: str, id_: int,
                 lang: Optional[str] = None, namespace: str = '') -> str:
    """Shorthand for returning the name of an entry based on its ID.

    The collection must use the "<collection>_id" ID field naming
    system and must contain a "name" key. If `lang` is specified, the
    corresponding locale will be assumed to be located therein.
    """
    # Input validation
    if id_ <= 0:
        raise ValueError('An ID must be greater than zero')
    # Perform a query for the given collection, using "<collection>_id" as the
    # field name
    query = Query(collection, namespace=namespace)
    query.add_term(f'{collection}_id', id_)
    # Perform the query and grab the "name" key.
    data = query.get()[0]['name']
    # If a language subkey has been specified, return it instead
    if lang is not None:
        return str(data[lang])
    # If the collection is "character", imply the "first" key.
    if collection == 'character':
        return str(data['first'])
    # Otherwise, return the "name" key directly (for non-localized strings)
    return str(data)
