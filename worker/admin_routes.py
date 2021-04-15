"""admin_routes module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import logging
from flask import request, jsonify, Blueprint

from worker.config import Config
from worker.data_adapter.pgsqldb import PqSqlDb

admin_services = Blueprint('admin_routes', __name__)

config = Config()
pgdb = PqSqlDb(config)

@admin_services.route('/pgsqlInit', methods=['POST'])
def init_pgsql():
    """
     tags:
       - services
     consumes:
       - application/json
     responses:
       200:
         description: Initialize PqgreSQL database successfully.
       400:
         description: Error
     """
    try:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS job
                (task_id       varchar(255)  PRIMARY KEY  NOT NULL,
                 workflow_id   varchar(255)  NOT NULL,
                 status        INT           NOT NULL,
                 content       TEXT          NOT NULL);
        """

        pgdb.execute(create_table_query)

        return jsonify(state=True, result="Succeed Initialize PostgreSQL"), 200
    except Exception as e:
        logging.error(f'Exception when initializing postgresql:{e}')
        return jsonify(error="unable to init postgresql"), 400


@admin_services.route('/dtInit', methods=['POST'])
def init_dt_table():
    """
     tags:
       - services
     consumes:
       - application/json
     responses:
       200:
         description: Initialize dt2fpath table successfully.
       400:
         description: Error
     """
    try:
        create_table_query = """
            CREATE TABLE IF NOT EXISTS dt2fpath
                (dt  varchar(255) PRIMARY KEY NOT NULL,
                fpath varchar(255) NOT NULL);
        """

        pgdb.execute(create_table_query)

        return jsonify(state=True, result="Succeed Initialize dt table"), 200
    except Exception as e:
        logging.error(f'Exception when initializing dt:{e}')
        return jsonify(error="unable to init dt"), 400


@admin_services.route('/dt2fpathCreate', methods=['POST'])
def insert_dt2fpath():
    """
     tags:
       - services
     consumes:
       - application/json
     parameters:
      - name: dt
        in: query
        description: dt to be inserted
        type: string
        required: true
        example: 123
      - name: fpath
        in: query
        description: the path of the file
        type: string
        required: true
        example: /some-url
     responses:
       200:
         description: dt and file_path successfully inserted.
       400:
         description: Error
     """
    try:
        dt = request.form.get("dt")
        fpath = request.form.get("fpath")

        insert_query = """
            INSERT INTO dt2fpath(dt,fpath)
            VALUES('{}','{}')
        """.format(dt, fpath)

        pgdb.execute(insert_query)

        return jsonify(state=True, result="Succeed Insert Dt2Path"), 200
    except Exception as e:
        logging.error(f'Exception when inserting dt and fpath to table:{e}')
        return jsonify(error="unable to insert dt and fpath to table"), 400
