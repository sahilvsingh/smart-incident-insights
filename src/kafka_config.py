# src/kafka_config.py
import os
import socket

def get_bootstrap_servers():
    """
    Inside Docker network -> 'kafka:9092'
    Outside -> 'localhost:29092' (as per docker-compose advertised listeners)
    You can override via KAFKA_BROKER env var.
    """
    override = os.getenv("KAFKA_BROKER")
    if override:
        return override
    try:
        socket.gethostbyname("kafka")
        return "kafka:9092"
    except socket.error:
        return "localhost:29092"
