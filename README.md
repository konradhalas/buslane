# buslane

[![Build Status](https://travis-ci.org/konradhalas/buslane.svg?branch=master)](https://travis-ci.org/konradhalas/buslane)
[![License](https://img.shields.io/pypi/l/buslane.svg)](https://pypi.python.org/pypi/buslane/)
[![Version](https://img.shields.io/pypi/v/buslane.svg)](https://pypi.python.org/pypi/buslane/)
[![Python versions](https://img.shields.io/pypi/pyversions/buslane.svg)](https://pypi.python.org/pypi/buslane/)

Simple message (event/command) bus.

## Installation

To install `buslane`, simply use `pip` (or `pipenv`):

```
$ pip install buslane
```

## Requirements

Minimum Python version supported by `buslane` is 3.6.

## Quick start

```python
from dataclasses import dataclass

from buslane.commands import Command, CommandHandler, CommandBus


@dataclass(frozen=True)
class RegisterUserCommand(Command):
    email: str
    password: str


class RegisterUserCommandHandler(CommandHandler[RegisterUserCommand]):

    def handle(self, command: RegisterUserCommand) -> None:
        assert command == RegisterUserCommand(
            email='john@lennon.com',
            password='secret',
        )


command_bus = CommandBus()
command_bus.register(handler=RegisterUserCommandHandler())
command_bus.execute(command=RegisterUserCommand(
    email='john@lennon.com',
    password='secret',
))
```

## About

This library makes it easier to create solutions based on messages. If you want to split event occurrence from its
handling, `buslane` is the way to go. It supports commands (single handler) and events (0 or multiple handlers)
approach.

## Motivation

This package could be probably replaced with a simple Python dictionary with messages classes as keys and ordinary
functions as values. Python is a dynamic language and we can implement such solution very easy, without any classes,
inheritance, methods overriding and so one. So why you should use `buslane`? Is it the *pythonic* approach?

First of all, `buslane` is very simple and tiny project. I was copying these few lines from project to project, so now I
don't have to.

Secondly, I'm a huge fan of type annotations. This a game changer in a project with a huge codebase. `buslane` has
type hints everywhere and it is based on [Python generics][python-generics]. In combination with such tools like
[`mypy`][mypy] you will be sure that you are doing (from types point of view) everything OK.

Message handler is a class instead of function, because you can easily inject your dependencies via `__init__`
parameters. Such class is very easy to test, you don't have to `mock.patch` everything. The interface is clear.

Last but not least - the `buslane` API is simple and well defined. You can extend it easily, e.g. log all of your
messages or store them in a database.

It can be used as a foundation of your CQRS-based system.

## Reference

`buslane` uses Python type annotations to properly register handler. To create your message you have to inherit from
`Event` or `Command` class. I recommend to use `dataclasses` module from Python 3.7 (or from PyPI) - command/event
should be just a simple bundle of immutable data, `dataclass` decorator makes it easy to create such class.

Handler should inherit from `EventHandler[T]` or `CommandHandler[T]`, where `T` is a class of your message.

### Events

You can register multiple or none handlers for a single event.

Classes:

- `Event`
- `EventHandler[Event]`
- `EventBus`

Exceptions:

- `WrongHandlerException`

#### Example

```python
from buslane.events import Event, EventHandler, EventBus


class SampleEvent(Event):
    pass


class SampleEventHandler(EventHandler[SampleEvent]):

    def handle(self, event: SampleEvent) -> None:
        pass


event_bus = EventBus()
event_bus.register(handler=SampleEventHandler())
event_bus.publish(event=SampleEvent())
```

### Commands

You have to register only single handler for the given command.

Classes:

- `Command`
- `CommandHandler[Command]`
- `CommandBus`

Exceptions:

- `MissingCommandHandlerException`
- `CommandHandlerRegisteredException`
- `WrongHandlerException`

#### Example

```python
from buslane.commands import Command, CommandHandler, CommandBus


class SampleCommand(Command):
    pass


class SampleCommandHandler(CommandHandler[SampleCommand]):

    def handle(self, command: SampleCommand) -> None:
        pass


command_bus = CommandBus()
command_bus.register(handler=SampleCommandHandler())
command_bus.execute(command=SampleCommand())
```

### Customizations

If you want to customize behaviour of your bus, you can override `handle` method from `EventBus` / `CommandBus` class.

The following example shows a bus which logs every event and process it in a thread.

```python
import logging
from concurrent.futures import ThreadPoolExecutor


class CustomEventBus(EventBus):

    def __init__(self, workers: int) -> None:
        super().__init__()
        self.logger = logging.getLogger()
        self.executor = ThreadPoolExecutor(max_workers=workers)

    def handle(self, event: Event, handler: EventHandler) -> None:
        self.logger.info(f'Handling event {event} by {handler}')
        self.executor.submit(handler.handle, event)
```

**Note**: This type of customization will be deprecated in the next release in favor of a plugins architecture.

## Authors

Created by [Konrad Hałas][halas-homepage].

[halas-homepage]: https://konradhalas.pl
[python-generics]: https://docs.python.org/3/library/typing.html#generics
[mypy]: https://github.com/python/mypy/
