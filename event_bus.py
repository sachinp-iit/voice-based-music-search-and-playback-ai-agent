# event_bus.py
from collections import defaultdict
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[Any], None]):
        """Subscribe a handler to an event type."""
        self.subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: Any):
        """Publish an event to all subscribers."""
        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                handler(data)
