#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import uuid
import os
from os.path import join

from worker.constant import ExecutorConfig, WorkerConfig


def get_random_name():
    uuid_str = uuid.uuid4().hex
    return uuid_str


def prepare_envir_dir():
    os.makedirs(WorkerConfig.WORKFLOW_SAVE_DIRPATH, exist_ok=True)
    os.makedirs(ExecutorConfig.RUNNER_DIRPATH, exist_ok=True)


def workflow_dir(workflow_id):
    save_dir_path = join(WorkerConfig.WORKFLOW_SAVE_DIRPATH, workflow_id)
    os.makedirs(save_dir_path, exist_ok=True)
    return save_dir_path


def runner_dir(runner_id):
    return join(ExecutorConfig.RUNNER_DIRPATH, runner_id)


def scheduler_dir():
    return f'{WorkerConfig.WORKER_DIRPATH}/worker/scheduler'


def executor_dir():
    return f'{WorkerConfig.WORKER_DIRPATH}/worker/executor'


def inputs_dirpath(path):
    return os.path.join(ExecutorConfig.INPUTS_DIRPATH, path)


def script_dirpath(path):
    return os.path.join(ExecutorConfig.SCRIPT_DIRPATH, path)


def prepare_running_dir(exec_path):
    os.makedirs(exec_path, exist_ok=True)
    os.makedirs(join(exec_path, 'inputs'), exist_ok=True)
    os.makedirs(join(exec_path, 'outputs'), exist_ok=True)
