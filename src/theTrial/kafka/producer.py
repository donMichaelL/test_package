from confluent_kafka import Producer

from ..log import get_logger

logger = get_logger("kafka-consumer")


class KafkaProducer:
    def __init__(self, config):
        self.producer = Producer(config)

    def send_message(self, topic: str, msg: str) -> None:
        def _acked(err, msg):
            if err is not None:
                logger.error(f"Failed to deliver message: {str(msg)}: {str(err)}")
            else:
                logger.info(f"Message produced: {str(msg.value())}")

        self.producer.produce(topic, value=msg, callback=_acked)
        self.producer.flush()
