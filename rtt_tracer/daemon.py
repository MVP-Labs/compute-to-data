"""Daemon module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

from rtt_tracer.routes import app
from rtt_tracer.config import Config
from rtt_tracer.utils import prepare_env_dir

if __name__ == '__main__':
    prepare_env_dir()
    app.run("0.0.0.0", Config().query_port, debug=True, use_reloader=False)
