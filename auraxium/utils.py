"""Shared utility methods used throughout Auraxium."""

from typing import Any, Dict, Union

# NOTE: The functions below are a dummy implementation for testing and will be
# revisited soon.


def nested_dict_get(dict_: Dict[str, Any], key: str) -> Any:
    """Nested dict key access."""
    nested_keys = key.split('.')
    while nested_keys:
        dict_ = dict_[nested_keys.pop(0)]
    return dict_


def nested_dict_pop(dict_: Dict[str, Any], key: str) -> Any:
    """Nested dict access and removal."""

    def nested_pop(sub_: Dict[str, Any], inner: str, *args: str) -> Any:
        if not args:
            return sub_.pop(inner)
        # pylint: disable=no-value-for-parameter
        value = nested_pop(sub_[inner], *args)
        if not sub_[inner]:
            del sub_[inner]
        return value

    outer, *inner = key.split('.')
    if not inner:
        return dict_.pop(outer)
    value = nested_pop(dict_[outer], *inner)
    if not dict_[outer]:
        del dict_[outer]
    return value
