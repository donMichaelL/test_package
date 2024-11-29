from confluent_kafka.cimpl import Message


def call_handlers(func_map: dict, msg: Message) -> None:
    topic, decoded_msg = msg.topic(), msg.value().decode("utf-8")

    message_fields = {
        "topic": topic,
        "partition": msg.partition(),
        "offset": msg.offset(),
        "key": msg.key().decode("utf-8") if msg.key() else None,
        "timestamp": msg.timestamp(),
    }

    for func, data_class in func_map.get(topic, []):
        func_args = len(func.__code__.co_varnames)
        if func_args == 0:
            func()
            continue

        instance = data_class.desirializer(decoded_msg)

        if func_args == 1:
            func(instance)
        else:
            func(instance, **message_fields)
