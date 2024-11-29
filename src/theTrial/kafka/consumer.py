from confluent_kafka import Consumer
from confluent_kafka import KafkaError

from ..log import get_logger
from ..utils import call_handlers

logger = get_logger("kafka-consumer")


class KafkaConsumer:
    def __init__(self, config):
        self.consumer = Consumer(config)

    def consume(self, func_map: dict) -> None:
        topics = list(func_map.keys())
        self.consumer.subscribe(topics)
        logger.info(f"Subscribed to topic: {topics}")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.error(
                            f"Reached end of partition: {msg.topic()} " f"[{msg.partition()}] at offset {msg.offset()}"
                        )
                    else:
                        logger.error(f"Error: {msg.error()}")
                else:
                    logger.info(f"Message received: {msg.value().decode('utf-8')} " f"topic {msg.topic()}")
                    call_handlers(func_map, msg)

        except KeyboardInterrupt:
            logger.info("Consumer interrupted")

        finally:
            self.consumer.close()
            logger.info("Consumer closed")
