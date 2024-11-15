import json

import pika


from typing import Dict

from config.settings import message_queue


class RabbitProducer:
    def __init__(self, params: Dict) -> None:
        # self.queue = params["queue"]
        self.username = params["username"]
        self.passwd = params["passwd"]
        self.host = params["host"]
        self.port = params["port"]

    def open_connection(self):

        credentials = pika.PlainCredentials(
            username=self.username,
            password=self.passwd,
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
            )
        )

    # 向队列发送消息
    def send_data(self, data, task_queue):
        self.open_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=task_queue)
        data = json.dumps(data).encode("utf-8")
        self.channel.basic_publish(
            exchange="",
            routing_key=task_queue,
            body=data,
        )
        self.close_connect()

    def close_connect(self):
        # self.channel.close()
        self.connection.close()


if __name__ == "__main__":
    rp = RabbitProducer(message_queue["rabbitmq"])
    rp.send_data({"type": "1", "message": ["1", "2", "3"]})
    rp.send_data({"type": "1", "message": ["1", "2", "3"]})
    rp.close_connect()
