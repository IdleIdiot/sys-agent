import re
import time
import math
import subprocess


class LinuxSniffApi:
    @classmethod
    def get_uptime(cls):
        cmd = "cat /proc/uptime|awk '{print $1}'"
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        # hour
        uptime = round(float(ps.communicate()[0]) / 3600, 2)
        return {"value1": uptime}

    @classmethod
    def get_pid(cls, process_path):
        cmd = "ps axf| grep '%s' | grep -v grep" % process_path
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        pid = ps.communicate()[0].split()[0]
        return pid

    @classmethod
    def get_disk_io_read_rate(cls, device_name="sda"):
        process = subprocess.Popen(["iostat", "-d"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return str(error)
        else:
            output = output.decode("utf-8")
            lines = output.split("\n")

            for line in lines[2:]:
                columns = line.split()

                if len(columns) > 0:
                    if device_name == columns[0]:
                        rd_sec = columns[2]
                        # Mbps?
                        return {"value1": rd_sec}

    @classmethod
    def get_disk_io_write_rate(cls, device_name="sda"):
        process = subprocess.Popen(["iostat", "-d"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return str(error)
        else:
            output = output.decode("utf-8")

            lines = output.split("\n")

            for line in lines[2:]:
                columns = line.split()

                if len(columns) > 0:
                    if device_name == columns[0]:
                        wr_sec = columns[3]
                        return {"value1": wr_sec}

    @classmethod
    def get_gpu_mem_percentage(cls, gpu_id):
        """
        If gpu_id not exists, raise Exception.
        """
        percent_gpu_mem_used = None
        cmd = "nvidia-smi --query-gpu=index,memory.used,memory.total --format=noheader,csv"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        outputs = result.stdout.decode("utf-8").split("\n")

        for output in outputs:
            if not output:
                continue
            output = output.split(",")

            if str(gpu_id) == str(output[0]):
                used = float(output[1].replace(" MiB", ""))
                total = float(output[2].replace(" MiB", ""))
                percent_gpu_mem_used = round(used / total, 4) * 100
                break
        if percent_gpu_mem_used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": percent_gpu_mem_used}

    @classmethod
    def get_gpu_mem(cls, gpu_id):
        """
        If gpu_id not exists, raise Exception.
        """
        used = None
        cmd = "nvidia-smi --query-gpu=index,memory.used,memory.total --format=noheader,csv"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        outputs = result.stdout.decode("utf-8").split("\n")

        for output in outputs:
            if not output:
                continue
            output = output.split(",")
            if str(gpu_id) == str(output[0]):
                used = float(output[1].replace(" MiB", ""))
                break
        if used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": used}

    @classmethod
    def get_gpu_power_percentage(cls, gpu_id: str):
        """
        If gpu_id not exists, raise Exception.
        """
        percent_gpu_power_used = None
        cmd = (
            "nvidia-smi --query-gpu=index,power.draw,power.limit --format=noheader,csv"
        )
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        outputs = result.stdout.decode("utf-8").split("\n")

        for output in outputs:
            if not output:
                continue
            output = output.split(",")

            if str(gpu_id) == str(output[0]):
                used = float(output[1].replace(" W", ""))
                total = float(output[2].replace(" W", ""))
                percent_gpu_power_used = round(used / total, 4) * 100
                break
        if percent_gpu_power_used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": percent_gpu_power_used}

    @classmethod
    def get_gpu_power(cls, gpu_id: str):
        """
        If gpu_id not exists, raise Exception.
        """
        used = None
        cmd = (
            "nvidia-smi --query-gpu=index,power.draw,power.limit --format=noheader,csv"
        )
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        outputs = result.stdout.decode("utf-8").split("\n")

        for output in outputs:
            if not output:
                continue
            output = output.split(",")

            if str(gpu_id) == str(output[0]):
                used = float(output[1].replace(" W", ""))
                break
        if used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": used}

    @classmethod
    def get_gpu_temperature(cls, gpu_id: str):
        # 执行 nvidia-smi 命令并捕获其输出
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,temperature.gpu",
                "--format=csv,noheader",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # 解析结果为字符串列表
        output = result.stdout.decode("utf-8").strip()

        # 将输出按行分割并提取每个GPU的信息
        lines = output.split("\n")

        for line in lines:
            parts = line.split(",")
            if str(parts[0]) == gpu_id:  # 检查是否匹配指定的gpu_id
                return {"value1": float(parts[1])}  # 返回温度值

        raise Exception(f"无法找到GPU ID {gpu_id} 的信息")

    @classmethod
    def get_npu_chip_power(cls, npu_id: str, chip_id: str):
        """
        If npu_id not exists, raise Exception.
        """
        percent_npu_chip_power = None
        cmd = f"npu-smi info -t power -i {npu_id} -c {chip_id}"
        cmd = cmd + " | awk '{print $5}'"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        percent_npu_chip_power_used = result.stdout.decode("utf-8").strip("\n")

        if percent_npu_chip_power_used is None:
            err_msg = f"Not have npu {npu_id} chip {chip_id} in this machine"
            raise Exception(err_msg)
        return {"value1": percent_npu_chip_power_used}

    @classmethod
    def get_npu_chip_mem(cls, npu_id: str, chip_id: str):
        """
        If npu_id not exists, raise Exception.
        """
        percent_npu_chip_mem_used = None
        cmd = f"npu-smi info -t usages -i {npu_id} -c {chip_id}"
        cmd = cmd + " | awk 'NR==2{print $5}'"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        percent_npu_chip_mem_used = result.stdout.decode("utf-8").strip("\n")

        if percent_npu_chip_mem_used is None:
            err_msg = f"Not have npu {npu_id} chip {chip_id} in this machine"
            raise Exception(err_msg)
        return {"value1": percent_npu_chip_mem_used}

    @classmethod
    def get_npu_chip_temp(cls, npu_id: str, chip_id: str):
        """
        If npu_id not exists, raise Exception.
        """
        percent_npu_chip_temp = None
        cmd = f"npu-smi info -t temp -i {npu_id} -c {chip_id}"
        cmd = cmd + " | awk '{print $4}'"
        result = subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        percent_npu_chip_temp = result.stdout.decode("utf-8").strip("\n")

        if percent_npu_chip_temp is None:
            err_msg = f"Not have npu {npu_id} chip {chip_id} in this machine"
            raise Exception(err_msg)
        return {"value1": percent_npu_chip_temp}


if __name__ == "__main__":
    print(LinuxSniffApi.get_gpu_temperature(0))
