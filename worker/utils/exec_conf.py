#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import copy

from worker.utils.utilities import inputs_dirpath, script_dirpath


class ExecutorConf(object):
    EXEC_TYPE = 'type'
    EXEC_INPUTS = 'inputs'
    EXEC_SCRIPT = 'script'
    EXEC_ARGS = 'args'
    EXEC_QUERY_PORTS = 'query_ports'
    EXEC_OUTPUTS = 'outputs'
    EXEC_REQUIREMENTS = 'requirements'

    def __init__(self, exec_type, inputs, script, args, rpc_ports, outputs, requirements):
        self._type = exec_type
        self._inputs = inputs
        self._script = script
        self._args = args
        self._rpc_ports = rpc_ports
        self._outputs = outputs
        self._requirements = requirements

    # 包括执行器类型、端口列表、内存磁盘、进程数等
    @property
    def requirements(self):
        return self._requirements

    @property
    def type(self):
        return self._type

    # 目前用不到，应该是dt标识符号
    @property
    def inputs(self):
        return self._inputs

    # 返回代码脚本的文件名, 如algo1.py
    @property
    def script(self):
        return self._script

    # 返回模型参数的文件名, 如args.json，该文件包括模型的隐层单元数、batch_size等
    @property
    def args(self):
        return self._args

    # 目前用不到,未来应该是daemon自动判断存哪，并作为某一阶段的输入的。先不管
    @property
    def outputs(self):
        return self._outputs

    @property
    def rpc_ports(self):
        return self._rpc_ports

    def as_dictionary(self):
        values = {
            self.EXEC_TYPE: self._type,
            self.EXEC_INPUTS: self._inputs,
            self.EXEC_SCRIPT: self._script,
            self.EXEC_ARGS: self._args,
            self.EXEC_QUERY_PORTS: self._rpc_ports,
            self.EXEC_OUTPUTS: self._outputs,
            self.EXEC_REQUIREMENTS: self._requirements
        }
        return values

    @classmethod
    def _parse_json(cls, exec_conf_dict):
        ecd = copy.deepcopy(exec_conf_dict)
        _type = ecd.pop(cls.EXEC_TYPE, None)
        _args = ecd.pop(cls.EXEC_ARGS, None)
        _query_ports = ecd.pop(cls.EXEC_QUERY_PORTS, None)
        _requirements = ecd.pop(cls.EXEC_REQUIREMENTS, None)
        _outputs = ecd.pop(cls.EXEC_OUTPUTS, None)
        _inputs = [inputs_dirpath(path) for path in ecd.pop(cls.EXEC_INPUTS, None)]
        _script = script_dirpath(ecd.pop(cls.EXEC_SCRIPT, None))
        return _type, _inputs, _script, _args, _query_ports, _outputs, _requirements

    @classmethod
    def from_json(cls, exec_conf_dict):
        _type, _inputs, _script, _args, _query_ports, _output, _requirements = cls._parse_json(exec_conf_dict)
        return cls(_type, _inputs, _script, _args, _query_ports, _output, _requirements)
