#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> Dog = record_factory('Dog', 'name weight owner')
>>> record_factory('Cat', ['2name', 'weight', 'owner'])
Traceback (most recent call last):
  ...
TypeError: All field names must be identifiers
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
('name', 'weight', 'owner')
>>> rex = Dog('Rex', 30)
Traceback (most recent call last):
  ...
TypeError: missing a required argument: 'owner'
>>> rex = Dog('Rex', 30, 'Bob', owner='Bob')
Traceback (most recent call last):
...
TypeError: multiple values for argument 'owner'
>>> rex = Dog('Rex', 30, 'Bob', master='Bob')
Traceback (most recent call last):
...
TypeError: got an unexpected keyword argument 'master'
"""
from collections.abc import Iterable
from typing import Union, Any, Iterator
from inspect import Signature, Parameter

FieldNames = Union[str, Iterable[str]]


def record_factory(cls_name: str, field_names: FieldNames) -> type[object]:
    slots = get_field_names(field_names)

    def __init__(self, *args, **kwargs):
        sig = Signature(
            Parameter(name=name, kind=Parameter.POSITIONAL_OR_KEYWORD) for name in slots
        )
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
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


def get_field_names(field_names: FieldNames) -> tuple[str, ...]:
    names: list[str] | Iterable[str]
    if isinstance(field_names, str):
        names = field_names.replace(",", " ").split()
    else:
        names = field_names
    if not all(n.isidentifier() for n in names):
        raise TypeError("All field names must be identifiers")
    return tuple(names)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
