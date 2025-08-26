from dotenv import load_dotenv
import os

load_dotenv()

# Kafka
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "incident-topic")

# PostgreSQL
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "incidentdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
