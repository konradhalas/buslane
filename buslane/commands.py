import abc
from typing import TypeVar, Generic, Type, Dict

from buslane.utils import get_generic_arg


class Command:
    pass


C = TypeVar('C', bound=Command)


class CommandHandler(abc.ABC, Generic[C]):

    @abc.abstractmethod
    def handle(self, command: C) -> None:
        pass


class CommandBusException(Exception):
    pass


class MissingCommandHandlerException(CommandBusException):
    pass


class CommandHandlerRegisteredException(CommandBusException):
    pass


class CommandBus:

    def __init__(self) -> None:
        self._handlers: Dict[Type[Command], CommandHandler] = {}

    def register(self, handler: CommandHandler):
        command_cls = get_generic_arg(type(handler), Command)
        if command_cls in self._handlers:
            raise CommandHandlerRegisteredException()
        self._handlers[command_cls] = handler

    def execute(self, command: Command) -> None:
        try:
            self.handle(command=command, handler=self._handlers[type(command)])
        except KeyError:
            raise MissingCommandHandlerException()

    def handle(self, command: Command, handler: CommandHandler) -> None:
        handler.handle(command)
