from flask import Flask, jsonify
from flask_cors import CORS
import json
from multiprocessing import Process
import time
import random
import shutil
import os
import signal

# 解析同目录下的config文件
config = json.load(open('config.json'))
print(config)

# 参考格式 Reference: https://github.com/ownership-labs/executor-interface
self_id = config['self_id']
addr_dict = config["addr_dict"]
comm = addr_dict["comm"]
running_url, running_port = comm.split(":")
inputs, outputs = config["input_data"], config["output_data"]


# 任务状态 Reference: https://github.com/ownership-labs/executor-interface/blob/main/executorCommon/StageManager.py
class JobStatus:
    STARTED = 0
    RUNNING = 1
    FINISHED = 2
    FAILED = 3
    READY_TO_QUIT = 4


# 测试环境
status = JobStatus.STARTED
print(f"EXECUTOR {self_id} ENTER STARTED STATUS")
app = Flask(__name__)
CORS(app)


# 功能函数
@app.route('/GetStatus', methods=['GET'])
def executor_status_query():
    global status
    if status == JobStatus.STARTED:
        status = JobStatus.RUNNING
        print(f"EXECUTOR {self_id} ENTER RUNNING STATUS")
        return jsonify(JobStatus.STARTED), 200
    elif status == JobStatus.RUNNING:
        if random.randint(0, 3) == 1:
            status = JobStatus.FAILED
            print(f"EXECUTOR {self_id} ENTER RUNNING STATUS")
        else:
            status = JobStatus.FINISHED
            shutil.copy(inputs[0], outputs[0])
            print(f"EXECUTOR {self_id} ENTER FINISHED STATUS")
        return jsonify(JobStatus.RUNNING), 200
    return jsonify(status), 200


@app.route('/CallExit', methods=['POST'])
def executor_exit():
    exit_executor()
    return jsonify("success"), 200


def exit_executor():
    pid = os.getpid()
    os.kill(pid, signal.SIGKILL)


print(f"{self_id} I'm Running")
app.run(running_url, port=running_port, debug=True, use_reloader=False)
