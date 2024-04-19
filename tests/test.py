import time


cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(cur_time)
from datetime import datetime, timedelta

# 获取当前时间
start_time = datetime.now()
end_time = start_time - timedelta(minutes=5)

start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
