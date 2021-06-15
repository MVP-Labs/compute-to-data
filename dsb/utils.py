"""Utils module."""
# Copyright 2021 The Compute-to-Data Authors
# SPDX-License-Identifier: LGPL-2.1-only

import os
import sqlite3

from dsb.constant import ExecConstant
from dsb.config import Config

config = Config()


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


def init_sqlite3_dbs():
    if os.path.exists(config.db_name):
        return

    conn = sqlite3.connect(config.db_name)
    cur = conn.cursor()

    sql_create_table = """
        CREATE TABLE IF NOT EXISTS  dtstore 
           (filepath  varchar(255) PRIMARY KEY NOT NULL,
            datatoken varchar(255));
    """
    cur.execute(sql_create_table)

    for filepath in config.assets_path:
        assert os.path.exists(
            filepath), 'please check the asset paths in the config'

        sql_insert_query = """
            INSERT INTO dtstore(filepath)
            VALUES('{}')
        """.format(filepath)

        cur.execute(sql_insert_query)

    conn.commit()


def get_dt_store(dt):
    conn = sqlite3.connect(config.db_name)
    cur = conn.cursor()

    sql_select_query = """
        SELECT filepath FROM dtstore WHERE datatoken = ?
    """
    cur.execute(sql_select_query, (dt,))

    store_path = cur.fetchall()

    if store_path:
        return store_path[0][0]

    return None
