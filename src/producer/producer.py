# src/producer/producer.py
import json
from typing import Optional
from kafka import KafkaProducer
from src.kafka_config import get_bootstrap_servers

producer = KafkaProducer(
    bootstrap_servers=get_bootstrap_servers(),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: str(k).encode("utf-8") if k is not None else None,
)

def send_message(topic: str, message: dict, key: Optional[str] = None):
    producer.send(topic, value=message, key=key)
    producer.flush()
    print(f"✅ Sent message to {topic}: key={key} value={message}")

if __name__ == "__main__":
    send_message("test-topic", {"msg": "hello"}, key="k1")
