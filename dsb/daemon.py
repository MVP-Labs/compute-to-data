"""Daemon module."""
# Copyright 2021 The Compute-to-Data Authors
# SPDX-License-Identifier: LGPL-2.1-only

from dsb.routes import app
from dsb.config import Config
from dsb.utils import prepare_env_dir, init_sqlite3_dbs

if __name__ == '__main__':
    prepare_env_dir()
    init_sqlite3_dbs()
    app.run("0.0.0.0", Config().query_port, debug=True, use_reloader=False)
