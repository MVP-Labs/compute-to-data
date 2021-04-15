"""routes module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import logging
import json
import subprocess
from flask import request, jsonify, Blueprint

from worker.config import Config
from worker.scheduler.task_manager import TaskManager
from worker.utils.utilities import get_random_name, workflow_dir, scheduler_dir
from worker.constant import ExecutorConfig

services = Blueprint('routes', __name__)

config = Config()


@services.route('/workflowLaunch', methods=['POST'])
def launch_workflow():
    """
     tags:
       - services
     consumes:
       - application/json
     parameters:
       - name: workflow
         in: body
         description: the workflow to be executed
         type: string
         required: True
         example: see file <examples/data/workflow.json>
     responses:
       200:
         description: workflow successfully launched.
       400:
         description: Error
     """
    try:
        data = request.form.get("workflow")
        workflow_json = json.loads(data)
        workflow_id = get_random_name()
        workflow_json["workflow_id"] = workflow_id
        save_path = workflow_dir(workflow_id) + '/workflow.json'
        json.dump(workflow_json, open(save_path, 'w'))

        # FIXME: 程序目前无法判断脚本是否启动成功
        shell_command = f'bash -c "cd {scheduler_dir()}; {ExecutorConfig.PYTHON_PATH} job_scheduler.py --workflow_path {save_path}"'
        subprocess.Popen(shell_command, shell=True)

        return jsonify(task_id=workflow_json["task_id"], workflow_id=workflow_id,
                       result="Workflow has been launched"), 200
    except Exception as e:
        logging.error(f'Exception when launching workflow:{e}')
        return jsonify(error="unable to launch workflow"), 400


@services.route('/jobStatusQuery', methods=['GET'])
def query_job_status():
    """
     tags:
       - services
     consumes:
       - application/json
     parameters:
      - name: task_id
        in: query
        description: task_id to be queried
        type: int
        required: true
        example: 123456
     responses:
       200:
         description: job_status successfully queried.
       400:
         description: Error
     return: job_status (int)
     """
    try:
        task_id = request.args.get("task_id")
        task_manager = TaskManager(config)
        job_status = task_manager.query_job_status(task_id)
        return jsonify(job_status), 200
    except Exception as e:
        logging.error(f'Exception when querying job status:{e}')
        return jsonify(error="unable to query job status"), 400
