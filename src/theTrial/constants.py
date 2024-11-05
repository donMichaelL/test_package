config_producers = {
    "bootstrap.servers": "localhost:9092",
}

config_consumers = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "theTrial-group-new",
    "auto.offset.reset": "latest",
    "enable.auto.commit": True,
}
