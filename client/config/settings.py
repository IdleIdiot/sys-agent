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
        "host": "10.121.177.161",
        "port": "5672",
        "queue": "system_metrics",
        "username": "rabbit-user",
        "passwd": "123456",
    },
}


database = {
    "elasticsearch": {
        "ip": "10.121.177.161",
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
    "1003": {
        "func": CommonSniffApi.get_net_send_io_by_interface,
        "args": "ens2f0",
        "alias": "net_send_io_rate",
    },
    "1004": {
        "func": CommonSniffApi.get_net_recv_io_by_interface,
        "args": "ens2f0",
        "alias": "net_recv_io_rate",
    },
    "1005": {
        "func": LinuxSniffApi.get_disk_io_read_rate,
        "args": "sda",
        "alias": "disk_read_io_rate",
    },
    "1006": {
        "func": LinuxSniffApi.get_disk_io_write_rate,
        "args": "sda",
        "alias": "disk_write_io_rate",
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
    "2009": {
        "func": LinuxSniffApi.get_gpu_mem_percentage,
        "args": "0",
        "alias": "gpu_0_mem_percentage",
    },
    "2010": {
        "func": LinuxSniffApi.get_gpu_mem_percentage,
        "args": "1",
        "alias": "gpu_1_mem_percentage",
    },
    "2011": {
        "func": LinuxSniffApi.get_gpu_mem_percentage,
        "args": "2",
        "alias": "gpu_2_mem_percentage",
    },
    "2012": {
        "func": LinuxSniffApi.get_gpu_mem_percentage,
        "args": "3",
        "alias": "gpu_3_mem_percentage",
    },
    "2013": {
        "func": LinuxSniffApi.get_gpu_power_percentage,
        "args": "0",
        "alias": "gpu_0_power_percentage",
    },
    "2014": {
        "func": LinuxSniffApi.get_gpu_power_percentage,
        "args": "1",
        "alias": "gpu_1_power_percentage",
    },
    "2015": {
        "func": LinuxSniffApi.get_gpu_power_percentage,
        "args": "2",
        "alias": "gpu_2_power_percentage",
    },
    "2016": {
        "func": LinuxSniffApi.get_gpu_power_percentage,
        "args": "3",
        "alias": "gpu_3_power_percentage",
    },
    "2017": {
        "func": LinuxSniffApi.get_gpu_temperature,
        "args": "0",
        "alias": "gpu_0_temperature",
    },
    "2018": {
        "func": LinuxSniffApi.get_gpu_temperature,
        "args": "1",
        "alias": "gpu_1_temperature",
    },
    "2019": {
        "func": LinuxSniffApi.get_gpu_temperature,
        "args": "2",
        "alias": "gpu_2_temperature",
    },
    "2020": {
        "func": LinuxSniffApi.get_gpu_temperature,
        "args": "3",
        "alias": "gpu_3_temperature",
    },
    "3001": {
        "func": LinuxSniffApi.get_npu_chip_mem,
        "args": "9, 0",
        "alias": "npu_9_chip_0_mem",
    },
    "3002": {
        "func": LinuxSniffApi.get_npu_chip_mem,
        "args": "13, 0",
        "alias": "npu_13_chip_0_mem",
    },
    "3011": {
        "func": LinuxSniffApi.get_npu_chip_power,
        "args": "9, 0",
        "alias": "npu_9_chip_0_power",
    },
    "3012": {
        "func": LinuxSniffApi.get_npu_chip_power,
        "args": "13, 0",
        "alias": "npu_13_chip_0_power",
    },
    "3021": {
        "func": LinuxSniffApi.get_npu_chip_temp,
        "args": "9, 0",
        "alias": "npu_9_chip_0_temp",
    },
    "3022": {
        "func": LinuxSniffApi.get_npu_chip_temp,
        "args": "13, 0",
        "alias": "npu_13_chip_0_temp",
    },
}
