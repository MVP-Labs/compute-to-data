import json
import unittest
from worker.run import app
import warnings
from worker.scheduler.task_manager import TaskManager
import random
from worker.config import Config

config = Config()


class RouteTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.task_manager = TaskManager(config)
        warnings.simplefilter('ignore', ResourceWarning)

    def test_correct_workflow(self):
        workflow = json.load(open("../examples/workflow.json"))
        workflow = json.dumps(workflow)
        response = self.client.post('/workflowLaunch', data=dict(workflow=workflow))
        data = json.loads(response.data)
        self.assertIn('task_id', data, '数据格式返回错误')
        self.assertEqual(data['result'], "Workflow has been launched", '数据返回错误')

    def test_empty_workflow(self):
        response = self.client.post('/workflowLaunch')
        self.assertEqual(response.status_code, 400)

    def test_job_status_with_task_id(self):
        # 随机生成或手动修改
        task_id = 14
        response = self.client.get(f'/jobStatusQuery?task_id={task_id}')
        data = json.loads(response.data)
        status = self.task_manager.query_job_status(task_id)
        if status:
            status = [list(e) for e in status]
        self.assertEqual(status, data)
        self.assertEqual(200, response.status_code)
