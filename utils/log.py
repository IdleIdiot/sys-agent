import os
import logging

from logging import Logger
from utils.common import get_project_root
from logging.handlers import TimedRotatingFileHandler


class FileLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复打印日志
        if not self.logger.handlers:
            # 创建一个handler，用于写入日志文件
            log_path = os.path.join(get_project_root(), "logs")
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            log_name = os.path.join(log_path, "mole.log")
            file_handler = TimedRotatingFileHandler(
                log_name, when="midnight", interval=1, backupCount=7
            )
            file_handler.setLevel(level)

            # 定义日志输出格式
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)

            # 将logger添加到handler里面
            self.logger.addHandler(file_handler)

    def get_logger(self) -> Logger:
        return self.logger


# 使用示例
if __name__ == "__main__":
    logger = FileLogger(__name__).get_logger()
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
