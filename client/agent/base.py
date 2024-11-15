import time
import copy
from typing import Dict

from config.tasks import *
from config import settings
from utils.log import FileLogger
from agent.api.producer import RabbitProducer

logger = FileLogger(__name__).get_logger()


class Agent:
    def __init__(self, task_name: Dict):
        self.tasks = eval(task_name)

        self.database = settings.database
        self.mq = settings.message_queue

        self.items_mapper = settings.items_mapper

        self.producer = RabbitProducer(self.mq["rabbitmq"])

    def handle(self):
        """
        通用处理：
            1. 读取 tasks 任务列表；
            2. 通过任务 ID 执行任务，并获取返回值；
            3. 将返回值装填到 template
            4. 信息写入到 消息队列
        """

        # test
        # 获取当前时间的时间戳（秒级别）
        # current_timestamp_seconds = time.time()

        # 将时间戳转换为毫秒级别
        # current_timestamp_milliseconds = current_timestamp_seconds

        # 打印结果
        # cur_time = int(current_timestamp_milliseconds)

        ##

        cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        logger.info(self.tasks)
        for task_type, task_info in self.tasks.items():
            results = []
            items = task_info["items"]

            for item in items:
                message = copy.deepcopy(task_info["template"])
                message["host_id"] = self.items_mapper["1000"]["func"](
                    self.items_mapper["1000"]["args"]
                )
                message["item_id"] = item
                # message["index_name"] = task_type
                message["agent_time"] = cur_time
                message["alias"] = self.items_mapper[item]["alias"]
                logger.info(message["alias"])

                try:
                    executor = self.items_mapper[item]
                    if executor["args"] == "":
                        rc = executor["func"]()
                    else:
                        rc = executor["func"](*executor["args"].split(","))
                    message.update(rc)

                    results.append(message)
                except Exception as e:
                    logger.warning(f"{e}")

                    logger.warning(f"{item} value can't read.")
            # 写入消息队列
            if len(results) > 0:
                logger.info(results)
                self.producer.send_data(results, task_type)


if __name__ == "__main__":
    # from config.settings import message_queue
    # from threading import Thread

    # consumer = RabbitConsumer(message_queue["rabbitmq"])
    # t = Thread(target=consumer.run)
    # t.start()

    ab = Agent("test_task")
    ab.handle()
    ab.producer.close_connect()
