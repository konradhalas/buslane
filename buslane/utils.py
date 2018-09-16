from typing import TypeVar, Type

T = TypeVar('T')


def get_generic_arg(generic_cls: Type, param_cls: Type[T]) -> Type[T]:
    for base in generic_cls.__orig_bases__:
        for arg in base.__args__:
            if issubclass(arg, param_cls):
                return arg
    raise ValueError()
