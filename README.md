# Compute-to-Data

## 概览

该项目基于分布式数据管理中间件DataToken和Rosetta隐私AI框架来实现可追溯且隐私保护的机器学习，由此构建了允许第三方执行远程计算的私域数据资产服务网格。rtt_tracer为基于flask架构的资产部署工具，帮助资产方快速定义本地计算服务并自动校验外部计算请求。client为面向第三方科学家的服务请求工具，以完成数据可用不可见情况下的机器学习。

## MVP体验

### 交互过程

考虑简单的联合风控场景，第三方金融科技公司C为两家银行A、B提供模型服务。银行A和银行B的客户数据位于私域数据库中，在保证数据隐私安全且操作可审计的情况下，允许接收第三方的联合风控模型，确认服务条款后授权以执行本地计算，最终对外提供结果。通过使用DataToken SDK，资产方可在区块链数据市场上对数据的计算权进行交易，完成数据资产货币化。

### 准备工作

首先需要部署dt-contracts合约，参考[部署教程](https://github.com/ownership-labs/dt-contracts)，并配置DataToken和隐私AI框架的运行环境，参考[SDK使用指南](https://github.com/ownership-labs/DataToken)和[Rosetta使用指南](https://github.com/LatticeX-Foundation/Rosetta)。随后，安装数据服务网格在运行时所需的依赖:

```
$ git clone https://github.com/ownership-labs/Compute-to-Data
$ cd Compute-to-Data
$ pip install -r requirements.txt
```

在测试示例中，Compute-to-Data需与dt-contracts和DataToken在同一目录。我们默认采用alaya私链部署时的四组公钥-私钥对，分别代表系统管理员、银行A、银行B和第三方C：

```
System Key:
  0xa2D4eD069A247bcBBeC037FCADd8C3A305b4e409
  4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
Bank A Key:
  0x7080b17af4b29F621A5Ef3B1802B2a778Af595d0
  5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173
Bank B key:
  0xFDEBd75565fE98c1B2659E82181D92B5C6943693
  eee795df5de4fc3636abfcfb6d1741665a903efa2b5ded74cea33ca92111b953
3rd-Party key:
  0x0148D6F66D4759aC7CcE98673dC9b75974E6bAe4
  6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```

### 运行demo

我们在./samples下提供了用于快速测试的配置文件、数据集、资产元信息、联合风控模型等。本地计算所需的资源、运行日志等被存储在./tests中，每一次计算将自动创建对应job_id的文件夹，自动获取所需的数据、模型和参数等。这相当于简单模拟一个私域计算沙箱。demo操作流程如下：

#### 系统管理员

系统管理员在./samples/op中配置联合模型代码及其元数据，随后发布代码以得到可信算子通证：
```
$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ python client/dt-cli.py system org --name 'org1' --desc 'test_org1' --address 0x7080b17af4b29F621A5Ef3B1802B2a778Af595d0 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
```
系统管理员注册银行A、银行B、第三方C为链上资产提供方:
```
$ python client/dt-cli.py system org --name 'org2' --desc 'test_org2' --address 0xFDEBd75565fE98c1B2659E82181D92B5C6943693 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
$ python client/dt-cli.py system org --name '3rd-party' --desc 'test_3rd' --address  0x0148D6F66D4759aC7CcE98673dC9b75974E6bAe4 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
$ python client/dt-cli.py system op --attr_file ./samples/op/rtt_op_attr.json --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
```

#### 银行A、B

银行A、B分别在./samples/data/下放置本地数据资产，并在./samples/ddo/中配置资产元数据，将联合模型的算子通证包含在其中，随后发布资产以得到数据通证：
```
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org1_feature_attr.json --private_key 5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org1_label_attr.json --private_key 5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org2_feature_attr.json --private_key eee795df5de4fc3636abfcfb6d1741665a903efa2b5ded74cea33ca92111b953
```
银行A、B分别配置./samples/config/中的配置文件，包括私钥、dt合约信息、服务端口、本地资产存储路径等。同时，打开两个新的终端，运行本地数据计算服务的flask程序：

```
$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ export CONFIG_FILE=./samples/config/org1_config.ini
$ python rtt_tracer/daemon.py

$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ export CONFIG_FILE=./samples/config/org2_config.ini
$ python rtt_tracer/daemon.py
```

#### 第三方公司C

公司C在./samples/ddo/中配置算法资产元数据，将银行A、B的数据资产通证包含在其中，指明所用服务并满足参数约束，随后发布资产以得到可组合数据通证：
```
python client/dt-cli.py asset cdt --attr_file ./samples/ddo/3rd_algo_attr.json --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```
随后，公司C可在链上创建任务工作，并向银行A、B发起远程计算：
```
python client/dt-cli.py job init --name 'test' --desc 'test_task' --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
python client/dt-cli.py job exec --task_id 1 --cdt 'dt:ownership:34940ace7bdacfff97f4c5dd348f523119fdf1c82aa3ec2bf99149e88499a961' --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```
输出结果可以在tests/{job_id}/outputs/rtt_log.txt中查看，之后将为第三方提供查询远程日志的功能。

#### 监管方

监管方可进行数据全生命周期追溯：
```
python client/dt-cli.py tracer dfs --prefix_path "dt:ownership:34940ace7bdacfff97f4c5dd348f523119fdf1c82aa3ec2bf99149e88499a961"
```