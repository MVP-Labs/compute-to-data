# worker

REST API for Worker of data services

This is part of the Ownership Protocol.

This is feature complete and is a BETA version.

## Starting the server locally

### Quick start

```bash
pip install ownership-worker
export WORKER_DIRPATH=<worker dirpath>

export CONFIG_FILE_PATH=$WORKER_DIRPATH/config.ini
export LOG_PATH=$WORKER_DIRPATH/logging.yaml

export WORKFLOW_SAVE_DIRPATH=$WORKER_DIRPATH/examples/workflow_save_dir/
export INPUTS_DIRPATH=$WORKER_DIRPATH/examples/inputs/
export SCRIPT_DIRPATH=$WORKER_DIRPATH/examples/script/
export RUNNER_DIRPATH=$WORKER_DIRPATH/examples/exec_script_dir/
export OUTPUTS_DIRPATH=$WORKER_DIRPATH/examples/outputs/

export PYTHONPATH=$PYTHONPATH:$WORKER_DIRPATH
python3

>>> from worker.run import app
>>> from worker.config import config
>>> app.run("0.0.0.0", config.worker_port, debug=True, use_reloader=False)
```

### Detailed steps

#### 1. Clone the repo

```bash
git clone https://github.com/ownership-labs/worker.git
cd worker/
```

#### 2. Virtual env

Before running locally we recommend to set up virtual environment:

```bash
conda create --name ownership python=3.8
conda activate ownership
```

#### 3. Dependencies

*PostgreSQL.* we recommend to build PostgreSQL with Docker(Optional).

*Make sure to change Host and Port of PostgreSQL in config.ini*

```bash
cd examples/
docker-compose up -d
```

#### 4. Requirements

Install all the requirements:

```bash
pip install -r requirements.txt
```

#### 5. Start the provider server

```bash
export WORKER_DIRPATH=<worker dirpath>

export CONFIG_FILE=$WORKER_DIRPATH/config.ini
export LOG_PATH=$WORKER_DIRPATH/logging.yaml

export WORKFLOW_SAVE_DIRPATH=$WORKER_DIRPATH/examples/workflow_save_dir/
export INPUTS_DIRPATH=$WORKER_DIRPATH/examples/inputs/
export SCRIPT_DIRPATH=$WORKER_DIRPATH/examples/script/
export RUNNER_DIRPATH=$WORKER_DIRPATH/examples/exec_script_dir/
export OUTPUTS_DIRPATH=$WORKER_DIRPATH/examples/outputs/

export PYTHONPATH=$PYTHONPATH:$WORKER_DIRPATH
python3 worker/run.py
```
