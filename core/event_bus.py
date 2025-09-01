# core/event_bus.py

from collections import defaultdict
from typing import Callable, Dict, List, Any


class EventBus:
    """
    Simple event bus for agent-to-agent communication.
    Agents can subscribe to events and publish messages.
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """Subscribe a handler to an event type."""
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Any) -> None:
        """Publish an event and notify all subscribers."""
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                handler(data)
