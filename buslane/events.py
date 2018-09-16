import abc
from collections import defaultdict
from typing import TypeVar, Generic, Type, Dict, List

from buslane.utils import get_generic_arg


class Event:
    pass


E = TypeVar('E', bound=Event)


class EventHandler(abc.ABC, Generic[E]):

    @abc.abstractmethod
    def handle(self, event: E) -> None:
        pass


class EventBus:

    def __init__(self):
        self._handlers: Dict[Type[Event], List[EventHandler]] = defaultdict(list)

    def register(self, handler: EventHandler):
        self._handlers[get_generic_arg(type(handler), Event)].append(handler)

    def publish(self, event: Event):
        for handler in self._handlers[type(event)]:
            handler.handle(event)
