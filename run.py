#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> Dog = record_factory('Dog', 'name weight owner')
>>> rex = Dog('Rex', 30, 'Bob')
>>> rex
Dog(name='Rex', weight=30, owner='Bob')
>>> name, weight, _ = rex
>>> name, weight
('Rex', 30)
>>> "{2}'s dog weighs {1}kg".format(*rex)
"Bob's dog weighs 30kg"
>>> rex.weight = 32
>>> rex
Dog(name='Rex', weight=32, owner='Bob')
>>> Dog.__mro__
(<class '__main__.Dog'>, <class 'object'>)
>>> Dog = record_factory('Dog', ['name', 'weight', 'owner'])
>>> Dog.__slots__
['name', 'weight', 'owner']
"""
from collections.abc import Iterable
from typing import Union, Any, Iterator

FieldNames = Union[str, Iterable[str]]


def record_factory(cls_name: str, field_names: FieldNames) -> type(object):
    slots = get_field_names(field_names)

    def __init__(self, *args, **kwargs):
        kw = {k: v for k, v in zip(slots, args)}
        kw.update(kwargs)
        for name, value in kw.items():
            setattr(self, name, value)

    def __iter__(self) -> Iterator[Any]:
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(f"{k}={v!r}" for k, v in zip(slots, self)),
        )

    clsdict = {
        "__init__": __init__,
        "__iter__": __iter__,
        "__repr__": __repr__,
        "__slots__": slots,
    }

    return type(cls_name, (object,), clsdict)


def get_field_names(field_names: FieldNames) -> tuple[str]:
    if isinstance(field_names, str):
        return field_names.replace(",", " ").split()
    else:
        return field_names


if __name__ == "__main__":
    import doctest

    doctest.testmod()
