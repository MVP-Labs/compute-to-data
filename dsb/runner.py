"""Runner module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

import os
import json
import shutil
import subprocess

from datatoken.service.job import JobService
from datatoken.store.asset_resolve import resolve_asset, resolve_op
from dsb.config import Config
from dsb.constant import ExecConstant
from dsb.utils import setup_job_dir, save_to_disk

config = Config()
job_service = JobService(config)


class Runner(object):
    def __init__(self):
        self.exec_path = None
        self._pid = -1

    @property
    def pid(self):
        return self._pid

    def prepare_resources(self, job_id, algo_dt, dt):

        exec_path = setup_job_dir(job_id)

        data_path = config.assets_path.get(dt)
        shutil.copy(data_path, os.path.join(exec_path, 'inputs'))

        op, args = job_service.fetch_exec_code(algo_dt, dt)

        save_to_disk(op, os.path.join(exec_path, 'rtt_op.py'))
        save_to_disk(json.dumps(args), os.path.join(
            exec_path, 'rtt_args.json'))

        self.exec_path = exec_path

    def execute(self):
        shell_command = f'bash -c "cd {self.exec_path}; {ExecConstant.PYTHON_PATH} rtt_op.py --config rtt_args.json"'
        self._pid = subprocess.Popen(shell_command, shell=True).pid

        return
