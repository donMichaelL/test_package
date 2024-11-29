import json
from unittest.mock import MagicMock

import pytest


class DummyDataClass:
    @staticmethod
    def desirializer(data):
        return {"deserialized_data": json.loads(data)}


class DummyDataClassWithoutDesirializer:
    pass


@pytest.fixture
def dummy_data_class():
    """Fixture for a valid data class with a desirializer method."""
    return DummyDataClass


@pytest.fixture
def dummy_data_class_without_desirializer():
    """Fixture for an invalid data class without a desirializer method."""
    return DummyDataClassWithoutDesirializer


@pytest.fixture
def mock_function():
    """Fixture to create a mock function with a configurable signature."""

    def _mock_function(arg_names=(), arg_count=0):
        func = MagicMock()
        func.__code__ = MagicMock()
        func.__code__.co_varnames = arg_names
        func.__code__.co_argcount = arg_count
        return func

    return _mock_function


@pytest.fixture
def mock_message():
    """Fixture for a mock Kafka message."""
    message = MagicMock()
    message.topic.return_value = "example-topic"
    message.value.return_value = b'{"key": "value"}'
    message.partition.return_value = 0
    message.offset.return_value = 123
    message.key.return_value = b"key"
    message.timestamp.return_value = (1, 16777216)
    message.headers.return_value = [("header_key", "header_value")]
    return message
