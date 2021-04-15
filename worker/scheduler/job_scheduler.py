"""JobScheduler module."""
#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import time
import argparse

from worker.config import Config
from worker.utils.workflow import Workflow
from worker.scheduler.task_manager import TaskManager
from worker.scheduler.process_manager import ProcessManager
from worker.executor.executor_runner import ExecutorRunner

config = Config()


class JobScheduler(object):
    def __init__(self, workflow_json):
        self.workflow = Workflow(json_filepath=workflow_json)
        self.task_manager = TaskManager(config)
        self.process_manager = ProcessManager(config)
        # TODO: 全局DAG调度网络，根据workflow结构
        # TODO: self.communicator =

    def init_or_recover_job(self):
        # 如果该job已被执行过，则不再执行已调度完成的内容
        status_index = self.task_manager.is_task_exists(self.workflow.task_id)
        if status_index:
            status_index = status_index[0][0]
            self.workflow.start_from_checkpoint(status_index + 1)
        else:
            self.task_manager.insert_new_job(self.workflow.task_id, self.workflow.workflow_id,
                                             self.workflow.as_dictionary())

    def start_workflow(self):
        # 目前是按stage划分来顺序执行的, 更好的写法应该是
        # TODO: 不断检查DAG依赖,找出可以并行的部分,为每个执行点判断资源，回收已执行部分的资源
        for ix, stage in enumerate(self.workflow.stages):
            # runners所有任务列表, unready为资源不足暂无法执行的任务
            runners, unready = self._exec_or_parallel_exec(stage)

            while not self._is_stage_finished(runners, unready):
                self._exec_if_possible(unready)
                time.sleep(3)

            self.task_manager.update_job_status(self.workflow.task_id, self.workflow.index + ix)

    def _exec_or_parallel_exec(self, stage):
        runners, unready = [], []

        for s, e, exec_conf in stage:
            runner = ExecutorRunner(exec_conf)
            runners.append(runner)

            runner.prepare_resources(self.workflow.workflow_path, s, e)

            if not self._is_available(runner.resources):
                unready.append(runner)
                continue

            runner.execute()
            self.process_manager.register(runner.pid)

        return runners, unready

    def _is_available(self, resources):
        return self.process_manager.alloc_resources(resources)

    def _exec_if_possible(self, unready):
        for runner in reversed(unready):
            if self._is_available(runner.resources):
                runner.execute()
                self.process_manager.register(runner.pid)
                unready.remove(runner)
        return

    def _is_stage_finished(self, runners, unready):
        for runner in reversed(runners):
            if runner.is_finished():
                runner.exit()
                self.process_manager.remove(runner.pid)
                runners.remove(runner)
            elif runner.is_running():
                return False
            elif runner.is_failed():
                if not runner.exit():
                    self.process_manager.kill(runner.pid)
                runner.restart()
                unready.append(runner)
                return False

        return True

    # 根据DAG判断多方依赖关系，更新最新情况，调用workflow.parallelizable()
    # def _update_dag_dependency(self):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workflow_path', type=str, required=True)

    args = parser.parse_args()

    job_scheduler = JobScheduler(workflow_json=args.workflow_path)
    job_scheduler.init_or_recover_job()
    job_scheduler.start_workflow()
