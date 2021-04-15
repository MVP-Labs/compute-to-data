"""PostgreSQL module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import psycopg2

class PqSqlDb(object):
    def __init__(self, config):
        self.connection = psycopg2.connect(user=config.db_user, password=config.db_password,
                                           host=config.db_host, port=config.db_port,
                                           database=config.database)
        self.cursor = self.connection.cursor()

    def execute_with_query(self, query: str):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.fetchall()

    def execute(self, query: str):
        self.cursor.execute(query)
        self.connection.commit()
