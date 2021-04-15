"""Config module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import os
from configparser import ConfigParser
from worker.constant import WorkerConfig

class Config:
    def __init__(self):
        config_parser = ConfigParser()
        config_path = WorkerConfig.CONFIG_FILE
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'config file does not exist in {config_path}')

        self.configuration = config_parser.read(config_path)
        
        self.db_user = config_parser.get('data-adapter', 'user')
        self.db_password = config_parser.get('data-adapter', 'password')
        self.db_host = config_parser.get('data-adapter', 'host')
        self.db_port = config_parser.get('data-adapter', 'port')
        self.database = config_parser.get('data-adapter', 'database')

        self.max_process = config_parser.get('process-manager', 'max-process')
        self.max_memory_used = config_parser.get('process-manager', 'max-memory-used')
