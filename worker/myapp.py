"""myapp module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import os
from flask import Flask
from flask_cors import CORS
from worker.constant import WorkerConfig

app = Flask(__name__)
CORS(app)

app.config['CONFIG_FILE'] = WorkerConfig.CONFIG_FILE

