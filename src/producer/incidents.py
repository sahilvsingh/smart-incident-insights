# src/producer/incidents.py
import time
from typing import Optional
from src.producer.producer import send_message
from src.ml.predict import predict_category

TOPIC = "incident-topic"

def send_incident(incident_id: str, description: str, category: Optional[str] = None):
    if category is None:
        category = predict_category(description)
    message = {
        "incident_id": str(incident_id),
        "description": description,
        "category": category,
    }
    send_message(TOPIC, message, key=str(incident_id))

if __name__ == "__main__":
    for i in range(5):
        send_incident(f"INC-{i}", f"Incident number {i} - payment retry failed")
        time.sleep(0.2)
