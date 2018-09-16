from unittest.mock import Mock

import pytest

from buslane.commands import Command, CommandHandler, C, CommandBus, MissingCommandHandlerException, \
    CommandHandlerRegisteredException


class SampleCommand(Command):
    pass


class SampleCommandHandler(CommandHandler[SampleCommand]):
    def handle(self, command: C) -> None:
        pass


def test_handle_command():
    bus = CommandBus()
    handler = SampleCommandHandler()
    handler.handle = Mock()
    bus.register(handler)
    command = SampleCommand()

    bus.handle(command)

    handler.handle.assert_called_once_with(command)


def test_handle_command_without_handler():
    bus = CommandBus()

    with pytest.raises(MissingCommandHandlerException):
        bus.handle(SampleCommand())


def test_register_command_handler_twice():
    bus = CommandBus()
    handler = SampleCommandHandler()
    bus.register(handler)

    with pytest.raises(CommandHandlerRegisteredException):
        bus.register(handler)
