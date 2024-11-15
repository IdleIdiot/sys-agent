import os
import json
import subprocess

from typing import Dict


def load_json_file(config_path: str) -> Dict:
    data = {}

    if not os.path.exists(config_path):
        return data

    with open(config_path) as f:
        data = json.loads(f.read())
    return data


# 若调用，则基本只能支持Linux系统，慎用
def execute_shell(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # 检查命令是否执行成功
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
