"""
2024年4月15日：
    message_template: 存入elasticsearch需要的信息,
    message_queue: mq server config,
    database: elasticsearch config,
    func_mapper, item mapper func and args,
"""

from sniff.common import CommonSniffApi


message_queue = {
    "rabbitmq": {
        "host": "10.121.177.70",
        "port": "5672",
        "queue": "server-test",
        "username": "rabbit-user",
        "passwd": "123456",
    },
}


database = {
    "elasticsearch": {
        "ip": "10.121.177.70",
        "port": 9200,
        "user": "",
        "pwd": "",
    },
}


items_mapper = {
    "1000": {
        "func": CommonSniffApi.get_ip_address,
        "args": "WLAN",
        "comment": "获取主机对应接口的IP作为host id，特殊用途，不应被配置为监控项",
    },
    "1001": {
        "func": CommonSniffApi.get_uptime,
        "args": "",
        "comment": "获取启动时间",
    },
    "1002": {
        "func": CommonSniffApi.get_cpu_percent,
        "args": "",
        "comment": "获取CPU占用百分比",
    },
    "1003": {
        "func": CommonSniffApi.get_memory_percent,
        "args": "",
        "comment": "获取内存占用百分比",
    },
}
