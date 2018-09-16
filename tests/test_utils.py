from typing import Generic, TypeVar

from buslane.utils import get_generic_arg


class BaseMessage:
    pass


T = TypeVar('T', bound=BaseMessage)


class BaseHandler(Generic[T]):
    pass


class Message(BaseMessage):
    pass


class Handler(BaseHandler[Message]):
    pass


def test_get_generic_arg():
    assert get_generic_arg(generic_cls=Handler, param_cls=BaseMessage) == Message
