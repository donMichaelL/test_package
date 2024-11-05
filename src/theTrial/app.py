from collections.abc import Callable
from functools import wraps

from . import kafka
from .constants import config_consumers
from .constants import config_producers
from .exceptions import MissingSerializeMethodError


class TheTrial:
    def __init__(self):
        self.producer = kafka.KafkaProducer(config_producers)
        self.consumer = kafka.KafkaConsumer(config_consumers)
        self.outopic_functions = []

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
        self.consumer.consume(["test", "another_test"])
        # for func in self.outopic_functions:
        #     func()
