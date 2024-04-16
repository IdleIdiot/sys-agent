import json

import pika


from typing import Dict

from config.settings import message_queue


class RabbitProducer:
    def __init__(self, params: Dict) -> None:
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

    # 向队列发送消息
    def send_data(self, data):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        data = json.dumps(data).encode("utf-8")
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=data,
        )

    def close_connect(self):
        # self.channel.close()
        self.connection.close()


if __name__ == "__main__":
    rp = RabbitProducer(message_queue["rabbitmq"])
    rp.send_data({"type": "1", "message": ["1", "2", "3"]})
    rp.send_data({"type": "1", "message": ["1", "2", "3"]})
    rp.close_connect()
