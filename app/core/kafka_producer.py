import json
import random
from datetime import datetime

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError, KafkaConnectionError, NodeNotReadyError
from fastapi import HTTPException

from app.core.airlogger import logger
from app.schemas.document.kafka_document_schema import Kafka_Document
from app.core.config import settings

producers = {}


async def create_producer() -> AIOKafkaProducer:
    """Creates new AIOKafkaProducer instance connected to kafka server.

    Will produce exactly one copy of message in kafka "parser" topic.
    :return: AIOKafkaProducer instance connected to bootstrap_server.
    """
    app_id = f"air_front_{random.randint(0, 10000)}"
    logger.info(f"Uvicorn App ID : {app_id}")

    try:
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.Kafka.KAFKA_BOOTSTRAP_SERVERS,
            client_id=app_id,
            enable_idempotence=True,
            retry_backoff_ms=3000,
            value_serializer=lambda msg: json.dumps(msg.__dict__).encode("utf-8"),
        )
        producers[settings.Kafka.KAFKA_TOPIC] = producer
        await producer.start()
        logger.info(f"Created producer for topic {settings.Kafka.KAFKA_TOPIC}")
        return producer

    except NodeNotReadyError as ke:
        logger.error(f"Error: Kafka producer connection error: ({ke})")
        raise HTTPException(
            status_code=400, detail="Could not transmit document to backend, Communication Error!"
        )

    except KafkaConnectionError as ke:
        logger.error(f"Error: Kafka producer connection error: ({ke})")
        raise HTTPException(
            status_code=400, detail="Could not transmit document to backend, Communication Error!"
        )
    except KafkaError as error:
        logger.error(f"Error: Kafka producer creation error: ({error})")
        raise HTTPException(
            status_code=400, detail="Could not transmit document to backend, Communication Error!"
        )


async def send_kafka_message(
        producer: AIOKafkaProducer, message: Kafka_Document
) -> None:
    """Sends provided message to "parser" topic via AIOKafkaProducer.

    :param producer: AIOKafkaProducer instance connected to bootstrap_server.
    :param message: Dict with key: values data to send via kafka topic.
    :return: None.
    """
    try:
        response = await producer.send_and_wait(settings.Kafka.KAFKA_TOPIC, message)
        send_time = datetime.fromtimestamp(response.timestamp / 1000)
        logger.info(
            f"Message was sent to topic '{response.topic}' at {send_time} IST"
        )

    except NodeNotReadyError as ke:
        logger.error(f"Error: Kafka producer connection error: ({ke})")
        raise HTTPException(
            status_code=400, detail="Could not transmit document to backend, Communication Error!"
        )

    except KafkaConnectionError as ke:
        logger.error(f"Error: Kafka producer connection error: ({ke})")

    except KafkaError as error:
        logger.error(f"Error: Kafka send message error: ({error})")
