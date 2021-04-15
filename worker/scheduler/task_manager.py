"""TaskManager module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

from worker.data_adapter.pgsqldb import PqSqlDb

class TaskManager(object):
    def __init__(self, config):
        self.pqsql_db = PqSqlDb(config)

    def insert_new_job(self, task_id: str, workflow_id: str, content):
        content = str(content).replace("'", "^")
        insert_table_query = """
            INSERT INTO job (task_id, workflow_id, status, content)
            VALUES('{}','{}','{}','{}')
        """.format(task_id, workflow_id, -1, content)
        self.pqsql_db.execute(insert_table_query)

    def update_job_status(self, task_id: str, status: int):
        update_table_query = """
            UPDATE job set status = '{}'
            WHERE task_id = '{}'
        """.format(status, task_id)
        self.pqsql_db.execute(update_table_query)

    def query_job_status(self, task_id: str):
        job_status_query = """
            SELECT COALESCE(status,null) FROM job
            WHERE task_id = '{}'
        """.format(task_id)
        return self.pqsql_db.execute_with_query(job_status_query)

    def is_task_exists(self, task_id: str):
        job_status_query = """
            SELECT COALESCE(status,null) FROM job
            WHERE task_id = '{}'
        """.format(task_id)
        return self.pqsql_db.execute_with_query(job_status_query)
