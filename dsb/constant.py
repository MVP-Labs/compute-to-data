"""Constant module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

import sys
from os import getenv
from os.path import join

class ExecConstant:
    CONFIG_FILE = getenv('CONFIG_FILE', './config.ini')
    EXEC_DIRPATH = getenv('EXEC_DIRPATH', './tests/')
    PYTHON_PATH = join(sys.exec_prefix, "bin", "python")
