#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import os
import json
from worker.utils.exec_conf import ExecutorConf
from worker.utils.utilities import workflow_dir


class Workflow(object):
    def __init__(self, task_id=None, task_name=None, json_filepath=None, dictionary=None):
        self._task_id = task_id
        self._task_name = task_name
        self._workflow_id = None
        self._stages = []
        self._index = 0

        if json_filepath:
            file_handle = open(json_filepath, 'r')
            self._read_dict(json.load(file_handle))
        elif dictionary:
            self._read_dict(dictionary)

    @property
    def task_id(self):
        return self._task_id

    @property
    def task_name(self):
        return self._task_name

    @property
    def workflow_id(self):
        return self._workflow_id

    @property
    def stages(self):
        return self._stages[self._index:]

    @property
    def index(self):
        return self._index

    def start_from_checkpoint(self, index):
        self._index = index

    @property
    def workflow_path(self):
        return workflow_dir(self._workflow_id)

    def as_dictionary(self):
        data = {'task_id': self._task_id, 'task_name': self._task_name}

        if self._workflow_id:
            data['workflow_id'] = self._workflow_id

        if self._stages:
            stage_values = []
            for stage in self._stages:
                exec_values = []
                for exec_conf in stage: exec_values.append(exec_conf[2].as_dictionary())
                stage_values.append(exec_values)
            data['stages'] = stage_values

        return data

    def _read_dict(self, values):
        self._task_id = values['task_id']
        self._task_name = values['task_name']
        self._workflow_id = values['workflow_id']
        self._stages = []

        s = 0
        for current_stage in values['stages']:
            current_stage_task = []
            e = 0
            for exec_value in current_stage:
                exec_conf = ExecutorConf.from_json(exec_value)
                current_stage_task.append((s, e, exec_conf))
                e = e + 1
            s = s + 1
            self._stages.append(current_stage_task)

    # TODO: 根据已完成的，返回当前可并行的部分
    # TODO: 暂时不用管
    # TODO: def parallelizable(self, finished_part):
    #     return
