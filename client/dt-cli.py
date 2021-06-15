"""DataToken client module."""
# Copyright 2021 The rtt-tracer Authors
# SPDX-License-Identifier: LGPL-2.1-only

import requests
import json
import argparse
import logging

from datatoken.web3.wallet import Wallet
from datatoken.web3.utils import add_ethereum_prefix_and_hash_msg
from datatoken.store.asset_resolve import resolve_asset
from datatoken.service.system import SystemService
from datatoken.service.asset import AssetService
from datatoken.service.job import JobService
from datatoken.service.tracer import TracerService
from datatoken.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = Config()

system_service = SystemService(config)
asset_service = AssetService(config)
job_service = JobService(config)
tracer_service = TracerService(config)


def register_org(args):
    account = Wallet(config.web3, private_key=args.private_key)

    system_service.register_enterprise(
        args.address, args.name, args.desc, account)
    system_service.add_provider(args.address, account)

    logger.info(f'register organizaton for address: {args.address}')

    return


def publish_op(args):
    account = Wallet(config.web3, private_key=args.private_key)

    with open(args.attr_file, 'r') as f:
        op_attr = json.load(f)

    metadata = op_attr.get('metadata')
    operation_file = op_attr.get('operation')
    params_file = op_attr.get('params')

    with open(operation_file, 'r') as f:
        operation = f.read()
    with open(params_file, 'r') as f:
        params = f.read()

    op_template = system_service.publish_template(
        metadata, operation, params, account)

    logger.info(f'publish op template with tid: {op_template.tid}')

    return


def mint_dt(args):
    account = Wallet(config.web3, private_key=args.private_key)

    with open(args.attr_file, 'r') as f:
        dt_attr = json.load(f)

    metadata = dt_attr.get('metadata')
    child_dts = dt_attr.get('child_dts')
    services = dt_attr.get('services')

    ddo = asset_service.generate_ddo(
        metadata, services, account.address, child_dts=child_dts, verify=True)
    asset_service.publish_dt(ddo, account)

    logger.info(f'mint data token with dt: {ddo.dt}')

    if not ddo.is_cdt:
        endpoint = ddo.services[0].endpoint

        data = {'store_path': args.store_path, 'dt': ddo.dt,
                'metadata': ddo.to_dict()}

        response = requests.post(f"http://{endpoint}/insertDtStore", data=json.dumps(data),
                                 headers={'content-type': 'application/json'}, timeout=5)

        if response.status_code != 200:
            raise Exception(response.content.decode('utf-8'))

    return ddo, account


def compose_cdt(args):
    cdt_ddo, account = mint_dt(args)

    for child_dt in cdt_ddo.child_dts:
        data, ddo = resolve_asset(child_dt, asset_service.dt_factory)
        endpoint = ddo.services[0].endpoint

        msg = f'{account.address}{cdt_ddo.dt}'
        msg_hash = add_ethereum_prefix_and_hash_msg(msg)
        signature = account.sign(msg_hash).signature.hex()

        data = {'algo_dt': cdt_ddo.dt, 'dt': child_dt, 'signature': signature}

        response = requests.post(f"http://{endpoint}/grantPermission", data=json.dumps(data),
                                 headers={'content-type': 'application/json'}, timeout=5)

        if response.status_code != 200:
            raise Exception(response.content.decode('utf-8'))

    asset_service.activate_cdt(cdt_ddo.dt, cdt_ddo.child_dts, account)

    logger.info(f'compose data token with cdt: {cdt_ddo.dt}')

    return


def init_task(args):
    account = Wallet(config.web3, private_key=args.private_key)

    task_id = job_service.create_task(args.name, args.desc, account)

    logger.info(f'init task with task_id: {task_id}')

    return


def start_exec(args):
    account = Wallet(config.web3, private_key=args.private_key)

    job_id = job_service.add_job(args.task_id, args.cdt, account)

    logger.info(f'submit job with job_id: {job_id}')

    _, cdt_ddo = resolve_asset(args.cdt, asset_service.dt_factory)

    for child_dt in cdt_ddo.child_dts:
        _, ddo = resolve_asset(child_dt, asset_service.dt_factory)
        endpoint = ddo.services[0].endpoint

        msg = f'{account.address}{job_id}'
        msg_hash = add_ethereum_prefix_and_hash_msg(msg)
        signature = account.sign(msg_hash).signature.hex()

        data = {'job_id': job_id, 'algo_dt': cdt_ddo.dt,
                'dt': child_dt, 'signature': signature}

        response = requests.post(f"http://{endpoint}/onPremiseCompute", data=json.dumps(data),
                                 headers={'content-type': 'application/json'}, timeout=5)

        if response.status_code != 200:
            raise Exception(response.content.decode('utf-8'))

    logger.info(f'start job execution for cdt: {args.cdt}')

    return


def dfs_lifecycle(args):

    found = tracer_service.trace_dt_lifecycle(args.prefix_path, prefix=[])    
    tree = tracer_service.tree_format(found)
    if tree:
        tracer_service.print_tree(tree, indent=[], final_node=True)

    logger.info(f'print asset sharing lifecycle for dt: {args.prefix_path}')

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG')
    sub_parsers = parser.add_subparsers(help='sub-command help')

    ######
    system_parser = sub_parsers.add_parser('system', help='system help')
    system_sub_parsers = system_parser.add_subparsers(
        help='system sub-command help')

    org_parser = system_sub_parsers.add_parser('org', help='organization help')
    org_parser.add_argument('--address', type=str, required=True)
    org_parser.add_argument('--name', type=str, required=True)
    org_parser.add_argument('--desc', type=str, required=True)
    org_parser.add_argument('--private_key', type=str, required=True)

    org_parser.set_defaults(func=register_org)

    op_parser = system_sub_parsers.add_parser('op', help='operation help')
    op_parser.add_argument('--attr_file', type=str, required=True)
    op_parser.add_argument('--private_key', type=str, required=True)

    op_parser.set_defaults(func=publish_op)

    ######
    asset_parser = sub_parsers.add_parser('asset', help='asset help')
    asset_sub_parsers = asset_parser.add_subparsers(
        help='asset sub-command help')

    dt_parser = asset_sub_parsers.add_parser('dt', help='data token help')
    dt_parser.add_argument('--attr_file', type=str, required=True)
    dt_parser.add_argument('--store_path', type=str, required=False)
    dt_parser.add_argument('--private_key', type=str, required=True)

    dt_parser.set_defaults(func=mint_dt)

    cdt_parser = asset_sub_parsers.add_parser(
        'cdt', help='composable data token help')
    cdt_parser.add_argument('--attr_file', type=str, required=True)
    cdt_parser.add_argument('--private_key', type=str, required=True)

    cdt_parser.set_defaults(func=compose_cdt)

    ######
    job_parser = sub_parsers.add_parser('job', help='job help')
    job_sub_parsers = job_parser.add_subparsers(
        help='job sub-command help')

    task_parser = job_sub_parsers.add_parser('init', help='init task help')
    task_parser.add_argument('--name', type=str, required=True)
    task_parser.add_argument('--desc', type=str, required=True)
    task_parser.add_argument('--private_key', type=str, required=True)

    task_parser.set_defaults(func=init_task)

    job_parser = job_sub_parsers.add_parser('exec', help='exec job help')
    job_parser.add_argument('--task_id', type=int, required=True)
    job_parser.add_argument('--cdt', type=str, required=True)
    job_parser.add_argument('--private_key', type=str, required=True)

    job_parser.set_defaults(func=start_exec)

    ######
    tracer_parser = sub_parsers.add_parser('tracer', help='tracer help')
    tracer_sub_parsers = tracer_parser.add_subparsers(
        help='tracer sub-command help')

    task_parser = tracer_sub_parsers.add_parser('dfs', help='dfs help')
    task_parser.add_argument('--prefix_path', type=str, required=True)
    task_parser.add_argument('--detailed', type=str, required=False)

    task_parser.set_defaults(func=dfs_lifecycle)

    ######
    args = parser.parse_args()
    args.func(args)
