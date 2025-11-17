#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> Dog = record_factory('Dog', 'name weight owner')  # <1>
>>> rex = Dog('Rex', 30, 'Bob')
>>> rex  # <2>
Dog(name='Rex', weight=30, owner='Bob')
>>> name, weight, _ = rex  # <3>
>>> name, weight
('Rex', 30)
>>> "{2}'s dog weighs {1}kg".format(*rex)  # <4>
"Bob's dog weighs 30kg"
>>> rex.weight = 32  # <5>
>>> rex
Dog(name='Rex', weight=32, owner='Bob')
>>> Dog.__mro__  # <6>
(<class 'factories.Dog'>, <class 'object'>)
>>> Dog = record_factory('Dog', ['name', 'weight', 'owner'])
>>> Dog.__slots__
('name', 'weight', 'owner')
"""
from collections.abc import Iterable
from typing import Union, Any, Iterator

FieldNames = Union[str, Iterable[str]]


def record_factory(cls_name: str, field_names: FieldNames) -> type(object):
    slots = get_field_names(field_names)

    def __init__(self, *args, **kwargs):
        for name, value in zip(slots, args):
            setattr(self, name, value)

    def __iter__(self) -> Iterator[Any]:
        for name in self.__slots__:
            yield getattr(self, name)

    def __repr__(self) -> str:
        return ", ".join(f"{k}={v}" for k, v in zip(slots, self))

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
    Dog = record_factory("Dog", "name weight owner")
    rex = Dog("Rex", 30, "Bob")
    print(rex)
