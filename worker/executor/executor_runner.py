"""ExecutorRunner module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import subprocess
import requests
import shutil
import os
from os.path import join, basename
import time
import json

from worker.utils.utilities import get_random_name, runner_dir, prepare_running_dir
from worker.constant import ExecutorConfig, JobStatus


class ExecutorRunner(object):
    def __init__(self, exec_conf):
        self._exec_conf = exec_conf
        self._pid = -1
        self.exec_path = ''

    @property
    def resources(self):
        # TODO: 拿出exec_conf的requirements里所需的query/compute端口、存储及内存等要求
        # TODO: 提供给process_manager统一分配管理，暂时不管
        return self._exec_conf.requirements

    @property
    def pid(self):
        return self._pid

    def prepare_resources(self, workflow_path, s, e):
        # TODO: 判断是否安装了对应类型的executor，先不管，默认都安装了
        # TODO: 开发者脚本中基于./inputs/路径写代码即可, 并不是远程数据实际存储路径
        # TODO: 输入部分先这样写，跑通为主。至于dt的解析放provider还是worker，后面我会判断并且自己执行的

        name = get_random_name()
        exec_path = runner_dir(name)
        prepare_running_dir(exec_path)
        for input_path in self._exec_conf.inputs:
            shutil.copy(input_path, join(exec_path, 'inputs'))
        shutil.copy(self._exec_conf.script, exec_path)
        config = self.generate_script_json(name)
        json.dump(config, open(join(exec_path, 'config.json'), 'w'))
        os.makedirs(f"{workflow_path}/outputs/", exist_ok=True)
        os.symlink(join(exec_path, 'outputs'), f"{workflow_path}/outputs/{s}_{e}")

        self.exec_path = exec_path

    ##  FIXME: 不要在workflow.py里去写跟郑非适配的部分   这部分可以我来沟通
    ##  FIXME: _inputs应该先用 exec_path/inputs/xx.csv
    def generate_script_json(self, name):
        values = {"self_id": name,
                  "addr_dict": self._exec_conf.rpc_ports,
                  "input_data": [join('./inputs', basename(input_path)) for input_path in self._exec_conf.inputs],
                  "output_data": [join('./outputs', basename(output_path)) for output_path in self._exec_conf.outputs],
                  "extra_paras": self._exec_conf.args}
        return values

    def execute(self):
        # FIXME: 比较推荐直接运行template.py，其中使用exec-interface来运行script.py。跟郑非讨论看看
        shell_command = f'bash -c "cd {self.exec_path}; {ExecutorConfig.PYTHON_PATH} {self._exec_conf.script}"'
        self._pid = subprocess.Popen(shell_command, shell=True).pid

        # 确保exec开始执行了,超过多少时间，直接认为exec启动失败。暂时不管
        while True:
            if self.is_running():
                break
            time.sleep(3)

    def restart(self):
        self._pid = -1

    def is_running(self):
        status = self._get_status()
        if status == JobStatus.RUNNING:
            return True
        else:
            return False

    # TODO: 检查失败的次数
    def is_failed(self):
        status = self._get_status()
        # 如果成功启动后，grpc某一时刻什么都查不到，也认为exec失败了
        if status or status == JobStatus.FAILED:
            return True
        else:
            return False

    def is_finished(self):
        status = self._get_status()
        if status and status == JobStatus.FINISHED:
            return True
        else:
            return False

    def exit(self):
        try:
            requests.post(self._query_exit_url()).text
            return True
        except:
            return False

    def _get_status(self):
        try:
            status = requests.get(self._query_state_url()).text
            return int(status)
        except:
            return None

    def _query_state_url(self):
        base_url = self._exec_conf.rpc_ports['comm']
        return f"http://{base_url}/GetStatus"

    def _query_exit_url(self):
        base_url = self._exec_conf.rpc_ports['comm']
        return f"http://{base_url}/CallExit"
