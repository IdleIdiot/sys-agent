import time
import argparse

from threading import Thread

from utils.log import FileLogger
from agent.base import Agent


logger = FileLogger(__name__).get_logger()


args = argparse.ArgumentParser()

args.add_argument(
    "--term",
    type=int,
    default=5,
    help="代理监控资源的周期（单位：秒）",
)

args.add_argument(
    "--task_name",
    type=str,
    default="base_task",
    required=False,
    help="在 config/tasks 下配置的任务集合名称",
)

args = args.parse_args()


def start_agent(term=5, task_name=""):
    agent = Agent(task_name)

    try:
        while True:
            agent.handle()
            time.sleep(term)
    except Exception as e:
        logger.error(e.message)
    finally:
        agent.producer.close_connect()
        exit(1)


if __name__ == "__main__":
    # 开启消费者监听
    # 用 logstash 服务替换了
    # consumer = RabbitConsumer()
    # t = Thread(target=consumer.run)
    # t.start()

    start_agent(
        term=args.term,
        task_name=args.task_name,
    )
