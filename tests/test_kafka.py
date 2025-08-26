# tests/test_kafka.py
import pytest
from unittest.mock import MagicMock
import src.producer.producer as producer_module


@pytest.fixture
def mock_kafka_producer(monkeypatch):
    mock_producer = MagicMock()
    # Patch the KafkaProducer in producer.py
    monkeypatch.setattr(producer_module, "producer", mock_producer)
    return mock_producer


def test_kafka_send_message(mock_kafka_producer):
    from src.producer.producer import send_message

    send_message("test-topic", {"msg": "hello"}, key="k1")

    mock_kafka_producer.send.assert_called_once_with(
        "test-topic",
        value={"msg": "hello"},
        key="k1"
    )
    mock_kafka_producer.flush.assert_called_once()
