"""ProcessManager module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import logging
import os
import signal

# FIXME: 暂时先不写该模块
class ProcessManager(object):
    def __init__(self, config):
        self.max_process_number = config.max_process
        self.max_memory_used = config.max_memory_used
        self.process_pids = []
        self.used_ports = []

    def register(self, pid):
        self.process_pids.append(pid)

    def remove(self, pid):
        self.process_pids.remove(pid)

    def kill(self, pid):
        try:
            os.kill(pid, signal.SIGKILL)
            logging.info(f"Have already kill pid {pid}")
        except OSError as e:
            logging.error(f"ERROR:No such pid to kill:{e}")

    # TODO:  在这里判断存在异步问题，需在worker层面实现统一的进程管理(可能也不是这种做法，下版直接用k8s)
    # FIXME: 如len(self.process_pids) = max_process_number -1 时 同时有两个进程使用alloc_resources
    def alloc_resources(self, resources):
        # resources为exec的requirements, 初版不管

        # if set(ports) & set(self.used_ports):
        #     logging.warning("PORTS RESOURCE NOT SATISFIED")
        #     return False
        #
        # if len(self.process_pids) > self.max_process_number:
        #     logging.warning("PROCESS RESOURCE NOT SATISFIED")
        #     return False

        return True
