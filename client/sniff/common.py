import time
import psutil

from socket import AddressFamily


class CommonSniffApi:
    @classmethod
    def get_time(cls):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @classmethod
    def get_cpu_percent(cls):
        cpu_percent = psutil.cpu_percent(interval=1)
        return {"value1": cpu_percent}

    @classmethod
    def get_memory_percent(cls):
        mem = psutil.virtual_memory()
        # print(f"总内存: {mem.total / (1024 ** 3):.2f} GB")
        # print(f"可用内存: {mem.available / (1024 ** 3):.2f} GB")
        # print(f"已用内存: {mem.used / (1024 ** 3):.2f} GB")
        return {"value1": mem.percent}

    @classmethod
    def get_disk_usage(cls, path="/"):
        sdiskusage = psutil.disk_usage(path)
        return sdiskusage.percent

    @classmethod
    def get_net_send_io_by_interface(cls, ifname="WLAN"):
        previous_net_io = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        current_net_io = psutil.net_io_counters(pernic=True)
        for interface, _ in psutil.net_if_addrs().items():
            if interface == ifname:
                # / (1024 ** 3)
                previous_send_bytes = round(previous_net_io[interface].bytes_sent, 2)
                current_send_bytes = round(current_net_io[interface].bytes_sent, 2)
                # Mbps
                net_sent_rate = (
                    (current_send_bytes - previous_send_bytes) * 8 / ((1 << 10) ** 1)
                )
                return {"value1": net_sent_rate}

    @classmethod
    def get_net_recv_io_by_interface(cls, ifname="WLAN"):
        previous_net_io = psutil.net_io_counters(pernic=True)
        time.sleep(1)
        current_net_io = psutil.net_io_counters(pernic=True)

        for interface, _ in psutil.net_if_addrs().items():
            if interface == ifname:
                # / (1024 ** 3)
                previous_recv_bytes = round(previous_net_io[interface].bytes_recv, 2)
                current_recv_bytes = round(current_net_io[interface].bytes_recv, 2)
                # Mbps
                net_recv_rate = (
                    (current_recv_bytes - previous_recv_bytes) * 8 / ((1 << 10) ** 1)
                )
                return {"value1": net_recv_rate}

    @classmethod
    def get_ip_address(cls, ifname):
        """
        Get IP address for a given network interface name.
        """
        for nic, addrs in psutil.net_if_addrs().items():
            if nic == ifname:
                for addr in addrs:
                    if addr.family == AddressFamily.AF_INET:
                        return addr.address
        return None


if __name__ == "__main__":
    result = CommonSniffApi.get_net_recv_io_by_interface("ens2f0")
    print(result)
    pass
