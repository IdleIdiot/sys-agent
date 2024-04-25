import re
import time
import math
import subprocess


class LinuxSniffApi:
    @classmethod
    def get_contain_inner_cpu_percent(cls, proc_name=""):
        cmd = "docker stats --no-stream | grep %s | awk '{print $3}'" % proc_name
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return ps.communicate()[0].replace("%", "").replace("\n", "")

    @classmethod
    def get_contain_inner_mem_percent(cls, proc_name=""):
        cmd = "docker stats --no-stream | grep %s | awk '{print $7}'" % proc_name
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        return ps.communicate()[0].replace("%", "").replace("\n", "")

    @classmethod
    def get_contain_inner_block_size(cls, proc_name=""):
        cmd = (
            "docker stats --no-stream | grep %s | awk '{print $11\" \"$13}'" % proc_name
        )
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        recvs = ps.communicate()[0].split()
        for i in range(len(recvs)):
            recv = recvs[i]
            if "kB" in recv:
                recv = float(recv.replace("kB", "")) * 1024
            elif "MB" in recv:
                recv = float(recv.replace("MB", "")) * 1024 * 1024
            elif "GB" in recv:
                recv = float(recv.replace("GB", "")) * 1024 * 1024 * 1024
            elif "B" in recv:
                recv = float(recv.replace("B", ""))
            recvs[i] = recv
        return recvs[0], recvs[1]  # Bytes

    @classmethod
    def get_cpu_percent(cls, proc_name=""):
        cpu_use_list = []
        if proc_name == "":
            cmd = "top  -b -n 1|sed -n '3p'"
        else:
            pid = cls.get_pid(proc_name)
            cmd = "ps -p {0} -o %cpu|sed -n '2p'".format(pid)
        for x in range(10):
            use_perc = 0
            ps = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            recv = ps.communicate()[0]
            if proc_name == "":
                m = re.search(",\s*([\d\.]+)\s*%?id\s*,", recv)
                if m:
                    use_perc = 100 - float(m.groups()[0])
            else:
                use_perc = float(recv)
            cpu_use_list.append(use_perc)
        return float(sum(cpu_use_list)) / len(cpu_use_list)

    @classmethod
    def get_host_mem_percent(cls):
        cmd = "free -m|grep Mem:|awk '{print $3/$2}'"
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        mem_percent = float(ps.communicate()[0].split()[0]) * 100
        return mem_percent

    @classmethod
    def get_uptime(cls):
        cmd = "cat /proc/uptime|awk '{print $1}'"
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        uptime = float(ps.communicate()[0])
        return int(uptime)

    @classmethod
    def get_pid(cls, process_path):
        cmd = "ps axf| grep '%s' | grep -v grep" % process_path
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        pid = ps.communicate()[0].split()[0]
        return pid

    @classmethod
    def get_proc_mem_rss(cls, proc_name):
        pid = cls.get_pid(proc_name)
        cmd = "cat /proc/%s/status|grep VmRSS|awk '{print $2}'" % (pid)
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        mem = float(ps.communicate()[0].split()[0]) * 1024
        return mem

    @classmethod
    def process_info(cls, processname):
        tmpinfo = {
            "pid": cls.get_pid(processname),
            "cpu": cls.get_cpu_percent(processname),
            "mem": cls.get_proc_mem_rss(processname),
            "agent_time": cls.get_time(),
        }
        return tmpinfo

    @classmethod
    def get_contain_pid(cls, process_path):
        cmd = "docker inspect -f '{{.State.Pid}}' %s" % (process_path)
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        pid = ps.communicate()[0].split()[0]
        return pid

    @classmethod
    def get_contain_cpu_percent(cls, process_path):
        cpu_use_list = []
        pid = cls.get_contain_pid(process_path)
        cmd = "ps -p {0} -o %cpu|sed -n '2p'".format(pid)
        for _ in range(10):
            ps = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
            recv = ps.communicate()[0]
            use_perc = float(recv)
            cpu_use_list.append(use_perc)
        return float(sum(cpu_use_list)) / len(cpu_use_list)

    @classmethod
    def get_contain_proc_mem_rss(cls, process_path):
        pid = cls.get_contain_pid(process_path)
        cmd = "cat /proc/%s/status|grep VmRSS|awk '{print $2}'" % (pid)
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        mem = float(ps.communicate()[0].split()[0]) * 1024
        return mem

    @classmethod
    def docker_process_info(cls, processname):
        tmpinfo = {
            "pid": cls.get_contain_pid(processname),
            "cpu": cls.get_contain_cpu_percent(processname),
            "mem": cls.get_contain_proc_mem_rss(processname),
            "agent_time": cls.get_time(),
        }
        return tmpinfo

    @classmethod
    def get_host_disk_usage(cls, path):
        cmd = "df -h|grep %s$|awk '{print $5}'" % (path)
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        mem = float(ps.communicate()[0].split()[0].replace("%", ""))
        return mem

    @classmethod
    def get_path_size(cls, path):
        cmd = "du -s %s" % path
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output = ps.communicate()[0]
        result = output.split()[0]
        return result

    @classmethod
    def get_error_log_line(cls, path):
        cmd = "cat %s | grep -i error | wc -l" % path
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output = ps.communicate()[0].split()[0]
        return output

    @classmethod
    def get_net_rate(cls, nic):
        cmd = "cat /proc/net/dev | grep -E '\s*%s\s*:' |awk '{print $2\" \"$10}'" % (
            nic
        )
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        recv = ps.communicate()[0]
        net_in_1 = float(recv.split()[0]) * 8
        net_out_1 = float(recv.split()[1]) * 8
        time.sleep(1)
        ps = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        recv = ps.communicate()[0]
        net_in_2 = float(recv.split()[0]) * 8
        net_out_2 = float(recv.split()[1]) * 8
        net_in = (net_in_2 - net_in_1) / 1024
        net_out = (net_out_2 - net_out_1) / 1024
        return net_in, net_out  # Kbps

    @classmethod
    def get_gpu_mem(cls, gpu_id):
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

            if gpu_id == output[0]:
                used = float(output[1].replace(" MiB", ""))
                total = float(output[2].replace(" MiB", ""))
                percent_gpu_mem_used = round(used / total, 4) * 100
                break
        if percent_gpu_mem_used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": percent_gpu_mem_used}

    @classmethod
    def get_gpu_power(cls, gpu_id: str):
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

            if gpu_id == output[0]:
                used = float(output[1].replace(" W", ""))
                total = float(output[2].replace(" W", ""))
                percent_gpu_power_used = round(used / total, 4) * 100
                break
        if percent_gpu_power_used is None:
            raise Exception(f"Not have gpu {gpu_id} in this machine")
        return {"value1": percent_gpu_power_used}


if __name__ == "__main__":
    LinuxSniffApi.get_gpu_mem("2")
