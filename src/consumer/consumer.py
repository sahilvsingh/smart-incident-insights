# src/consumer/consumer.py
import json
import logging
from kafka import KafkaConsumer
from src.kafka_config import get_bootstrap_servers
from src.db.queries import insert_incident

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

TOPIC = "incident-topic"
GROUP_ID = "smart-incident-consumers"

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=get_bootstrap_servers(),
        group_id=GROUP_ID,
        enable_auto_commit=True,
        auto_offset_reset="latest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        key_deserializer=lambda k: k.decode("utf-8") if k is not None else None,
    )
    logger.info("🎧 Consumer listening on topic=%s brokers=%s", TOPIC, get_bootstrap_servers())
    for msg in consumer:
        value = msg.value
        incident_id = value.get("incident_id")
        description = value.get("description")
        category = value.get("category")
        row = insert_incident(incident_id, description, category)
        logger.info("💾 Inserted/Updated incident: %s", row)

if __name__ == "__main__":
    main()
