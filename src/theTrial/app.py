from collections import defaultdict
from collections.abc import Callable
from functools import wraps

from . import kafka
from .constants import config_consumers
from .constants import config_producers
from .exceptions import MissingSerializeMethodError
from .utils import validate_decorated_function


class TheTrial:
    def __init__(self):
        self.producer = kafka.KafkaProducer(config_producers)
        self.consumer = kafka.KafkaConsumer(config_consumers)
        self.outopic_functions = []
        self.intopic_functions = defaultdict(list)

    def intopic(self, topic: str) -> Callable:
        """
        Decorator to register a function to consume messages from a specific Kafka topic.
        """

        def decorator(func: Callable) -> Callable:
            func, data_class = validate_decorated_function(func)
            self.intopic_functions[topic].append((func, data_class))
            return func

        return decorator

    def outopic(self, topic: str, **options) -> Callable:
        """
        Decorator to send the result of a function to a specific Kafka topic.

        :param topic: The Kafka topic.
        #TODO: To be defined
        :param options: Additional options for the decorator.
        :return: The decorated function.
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def _wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not hasattr(result, "serializer") or not callable(result.serializer):
                    raise MissingSerializeMethodError(result)
                self.producer.send_message(topic=topic, msg=result.serializer())

            self.outopic_functions.append(_wrapper)
            return _wrapper

        return decorator

    def run(self):
        """Run the application, prompting for input."""
        self.consumer.consume(self.intopic_functions)
        # for func in self.outopic_functions:
        #     func()
