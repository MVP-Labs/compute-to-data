"""Utils module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

import os
import json

from rtt_tracer.constant import ExecConstant


def prepare_env_dir():
    os.makedirs(ExecConstant.EXEC_DIRPATH, exist_ok=True)


def setup_job_dir(job_id):
    exec_path = os.path.join(ExecConstant.EXEC_DIRPATH, f'job_{job_id}')
    os.makedirs(exec_path, exist_ok=True)
    os.makedirs(os.path.join(exec_path, 'inputs'), exist_ok=True)
    os.makedirs(os.path.join(exec_path, 'outputs'), exist_ok=True)

    return exec_path


def save_to_disk(data, save_path):
    with open(save_path, 'w') as f:
        f.write(data)

    return
