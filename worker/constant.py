"""constant module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

from os import getenv
import sys
from os.path import join


class WorkerConfig:
    CONFIG_FILE = getenv('CONFIG_FILE', './config.ini')
    LOG_PATH = getenv('LOG_PATH', './logging.yaml')
    WORKER_DIRPATH = getenv('WORKER_DIRPATH', '.')
    WORKFLOW_SAVE_DIRPATH = getenv('WORKFLOW_SAVE_DIRPATH', '/tmp/workflow')


class ExecutorConfig:
    RUNNER_DIRPATH = getenv('RUNNER_DIRPATH', '/tmp/runner')
    INPUTS_DIRPATH = getenv('INPUTS_DIRPATH', './examples/inputs')
    SCRIPT_DIRPATH = getenv('SCRIPT_DIRPATH', './examples/script/')
    PYTHON_PATH = join(sys.exec_prefix, "bin", "python")


class JobStatus:
    RUNNING = 1
    FINISHED = 2
    FAILED = 3
