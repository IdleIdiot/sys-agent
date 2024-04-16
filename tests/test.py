import time


cur_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
print(cur_time)

# 获取当前时间的时间戳（秒级别）
current_timestamp_seconds = time.time()

# 将时间戳转换为毫秒级别
current_timestamp_milliseconds = current_timestamp_seconds * 1000

# 打印结果
print(int(current_timestamp_milliseconds))
print(1713229649300)
