from typing import TypeVar, Type

T = TypeVar('T')


class WrongHandlerException(Exception):
    pass


def get_message_cls(handler_cls: Type, base_message_cls: Type[T]) -> Type[T]:
    if hasattr(handler_cls, '__orig_bases__'):
        for base in handler_cls.__orig_bases__:
            if base.__args__:
                for arg in base.__args__:
                    try:
                        if issubclass(arg, base_message_cls):
                            return arg
                    except TypeError:
                        pass
    raise WrongHandlerException()
