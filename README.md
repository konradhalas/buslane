# buslane

Simple message (event/command) bus. Work in progress.

## Example


```
from dataclasses import dataclass

from buslane.commands import Command, CommandHandler, CommandBus
from buslane.events import EventBus, Event, EventHandler


@dataclass
class RegisterUserCommand(Command):
    name: str
    email: str
    password: str


@dataclass
class UserRegisteredEvent(Event):
    name: str
    email: str


class RegisterUserCommandHandler(CommandHandler[RegisterUserCommand]):
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def handle(self, command: RegisterUserCommand) -> None:
        ...
        self.event_bus.publish(event=UserRegisteredEvent(
            name=command.name,
            email=command.email,
        ))


class UserRegisteredEventHandler(EventHandler[UserRegisteredEvent]):
    def handle(self, event: UserRegisteredEvent) -> None:
        ...


event_bus = EventBus()
event_bus.register(UserRegisteredEventHandler())
command_bus = CommandBus()
command_bus.register(RegisterUserCommandHandler(event_bus=event_bus))
command_bus.handle(command=RegisterUserCommand(
    name='John Lennon',
    email='john@lennon.com',
    password='secret',
))

```
