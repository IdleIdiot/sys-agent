"""
2024年4月15日：
    message_template: 存入elasticsearch需要的信息,
    message_queue: mq server config,
    database: elasticsearch config,
    func_mapper, item mapper func and args,
"""

from sniff.common import CommonSniffApi
from sniff.linux import LinuxSniffApi


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
        "args": "ens2f0",
        "alias": "host_id",
    },
    "1001": {
        "func": CommonSniffApi.get_cpu_percent,
        "args": "",
        "alias": "cpu_percent",
    },
    "1002": {
        "func": CommonSniffApi.get_memory_percent,
        "args": "",
        "alias": "mem_percent",
    },
    "2001": {
        "func": LinuxSniffApi.get_gpu_mem,
        "args": "0",
        "alias": "gpu_0_mem",
    },
    "2002": {
        "func": LinuxSniffApi.get_gpu_mem,
        "args": "1",
        "alias": "gpu_1_mem",
    },
    "2003": {
        "func": LinuxSniffApi.get_gpu_mem,
        "args": "2",
        "alias": "gpu_2_mem",
    },
    "2004": {
        "func": LinuxSniffApi.get_gpu_mem,
        "args": "3",
        "alias": "gpu_3_mem",
    },
    "2005": {
        "func": LinuxSniffApi.get_gpu_power,
        "args": "0",
        "alias": "gpu_0_power",
    },
    "2006": {
        "func": LinuxSniffApi.get_gpu_power,
        "args": "1",
        "alias": "gpu_1_power",
    },
    "2007": {
        "func": LinuxSniffApi.get_gpu_power,
        "args": "2",
        "alias": "gpu_2_power",
    },
    "2008": {
        "func": LinuxSniffApi.get_gpu_power,
        "args": "3",
        "alias": "gpu_3_power",
    },
}
