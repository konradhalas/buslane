from typing import Generic, TypeVar

import pytest

from buslane.utils import get_message_cls, WrongHandlerException


class BaseMessage:
    pass


T = TypeVar('T', bound=BaseMessage)


class BaseHandler(Generic[T]):
    pass


class Message(BaseMessage):
    pass


class Handler(BaseHandler[Message]):
    pass


class WrongHandler(BaseHandler):
    pass


def test_get_message_cls_should_return_correct_class():
    assert get_message_cls(handler_cls=Handler, base_message_cls=BaseMessage) == Message


def test_get_message_cls_should_raise_exception():
    with pytest.raises(WrongHandlerException):
        assert get_message_cls(handler_cls=WrongHandler, base_message_cls=BaseMessage)
