import json
import pika

from threading import Thread

from utils.log import FileLogger
from config.settings import message_queue
from scheduler.storage import ElasticsearchClient

logger = FileLogger(__name__).get_logger()


client = ElasticsearchClient()


def callback(ch, method, properties, body: bytes):
    # 接受消息后写入 elasticsearch
    data_items = json.loads(body.decode("utf-8"))
    logger.info(f"Received {data_items}")

    wait_delete = []

    for index_name, data_item in data_items.items():
        if data_item:
            if index_name not in wait_delete:
                wait_delete.append(index_name)
            client.create_index(index_name=index_name)
            client.bulk_index_documents(index_name, data_item)
            logger.info(f"Storage: {data_item}")

    for index_name in wait_delete:
        client.delete_old_data(index_name=index_name)
    # ch.basic_ack(delivery_tag=method.delivery_tag)


class RabbitConsumer:
    def __init__(self) -> None:
        params = message_queue["rabbitmq"]

        self.queue = params["queue"]
        credentials = pika.PlainCredentials(
            username=params["username"],
            password=params["passwd"],
        )
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=params["host"],
                port=params["port"],
                credentials=credentials,
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def run(self):
        self.channel.basic_consume(
            queue=self.queue,
            auto_ack=True,
            on_message_callback=callback,
        )
        self.channel.start_consuming()


if __name__ == "__main__":
    consumer = RabbitConsumer(message_queue["rabbitmq"])
    t = Thread(target=consumer.run)
    t.start()
