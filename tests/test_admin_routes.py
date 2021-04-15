import json
import unittest
from worker.run import app
import warnings
from worker.scheduler.task_manager import TaskManager
from worker.config import Config

config = Config()

class AdminRouteTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        self.task_manager = TaskManager(config)
        warnings.simplefilter('ignore', ResourceWarning)

    def test_init_pgsql(self):
        response = self.client.post('/pgsqlInit')
        data = json.loads(response.data)
        self.assertEqual(data['result'], "Succeed Initialize PostgreSQL", '数据返回错误')

    def test_init_dt_table(self):
        response = self.client.post('/dtInit')
        data = json.loads(response.data)
        self.assertEqual(data['result'], "Succeed Initialize dt table", '数据返回错误')

    def test_insert_dt2fpath(self):
        dt, fpath = '123123123', '/data/input/123.csv'
        response = self.client.post('/dt2fpathCreate', data=dict(dt=dt, fpath=fpath))
        data = json.loads(response.data)
        self.assertEqual(data['result'], "Succeed Insert Dt2Path", '数据插入成功')
