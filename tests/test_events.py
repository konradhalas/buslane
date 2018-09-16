from unittest import mock

from buslane.events import Event, EventHandler, EventBus


class SampleEvent(Event):
    pass


class SampleEventHandler(EventHandler[SampleEvent]):

    def handle(self, event: SampleEvent) -> None:
        pass


def test_handle_event():
    bus = EventBus()
    handler = SampleEventHandler()
    handler.handle = mock.Mock()
    bus.register(handler)
    event = SampleEvent()

    bus.publish(event)

    handler.handle.assert_called_once_with(event)


def test_handle_event_by_multiple_handlers():
    bus = EventBus()
    first_handler = SampleEventHandler()
    first_handler.handle = mock.Mock()
    second_handler = SampleEventHandler()
    second_handler.handle = mock.Mock()
    bus.register(first_handler)
    bus.register(second_handler)
    event = SampleEvent()

    bus.publish(event)

    first_handler.handle.assert_called_once_with(event)
    second_handler.handle.assert_called_once_with(event)
