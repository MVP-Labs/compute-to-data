"""Routes module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

import logging
import json
from flask_cors import CORS
from flask import Flask, request, jsonify

from datatoken.service.asset import AssetService
from datatoken.service.job import JobService

from dsb.config import Config
from dsb.runner import Runner

app = Flask(__name__)
CORS(app)

config = Config()

owner_address = config.wallet.address

asset_service = AssetService(config)
job_service = JobService(config)


@app.route('/grantPermission', methods=['POST'])
def grant_permission():
    """
     tags:
       - services
     consumes:
       - application/json
     parameters:
       - name: algo_dt
         in: query
         description: the algorithm data token
         type: string
         required: True
       - name: dt
         in: query
         description: the data token owned by this provider
         type: string
         required: True
       - name: signature
         in: query
         description: the signature signed by aggregator
         type: string
         required: True
     responses:
       200:
         description: Success
       400:
         description: Error
     """
    try:
        data = json.loads(request.get_data())

        algo_dt = data.get("algo_dt")
        dt = data.get("dt")
        signature = data.get("signature")

        if not config.assets_path.get(dt):
            logging.error('Asset is not available now')
            return jsonify(error="Error"), 400

        if not asset_service.check_service_terms(algo_dt, dt, owner_address, signature):
            logging.error('Service agreements are not satisfied')
            return jsonify(error="Error"), 400

        asset_service.grant_dt_perm(dt, algo_dt, config.wallet)

        return jsonify(algo_dt=algo_dt, dt=dt, result="Success"), 200
    except Exception as e:
        logging.error(f'Exception when granting permission: {e}')
        return jsonify(error="Error"), 400


@app.route('/onPremiseCompute', methods=['POST'])
def on_premise_compute():
    """
     tags:
       - services
     consumes:
       - application/json
     parameters:
       - name: job_id
         in: query
         description: the job id for computation
         type: int
         required: True
       - name: algo_dt
         in: query
         description: the algorithm data token
         type: string
         required: True
       - name: dt
         in: query
         description: the data token owned by this provider
         type: string
         required: True
       - name: signature
         in: query
         description: the signature signed by consumer
         type: string
         required: True
     responses:
       200:
         description: Success
       400:
         description: Error
     """
    try:
        data = json.loads(request.get_data())

        job_id = data.get("job_id")
        algo_dt = data.get("algo_dt")
        dt = data.get("dt")
        signature = data.get("signature")

        if not config.assets_path.get(dt):
            logging.error('Asset is not available now')
            return jsonify(error="Error"), 400

        if not job_service.check_remote_compute(algo_dt, dt, job_id, owner_address, signature):
            logging.error('Remote access is not allowed')
            return jsonify(error="Error"), 400

        runner = Runner()
        runner.prepare_resources(job_id, algo_dt, dt)
        runner.execute()

        return jsonify(job_id=job_id, algo_dt=algo_dt, dt=dt, result="Success"), 200
    except Exception as e:
        logging.error(f'Exception when lauching computation: {e}')
        return jsonify(error="Error"), 400
