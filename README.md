# Compute-to-Data

## 概览

该项目基于分布式数据管理中间件DataToken和Rosetta隐私AI框架来实现可追溯且隐私保护的机器学习，由此构建了允许第三方执行远程计算的私域数据资产服务网格。rtt_tracer为基于flask架构的资产部署工具，帮助资产方快速定义本地计算服务并自动校验外部计算请求。client为面向第三方科学家的服务请求工具，以完成数据可用不可见情况下的机器学习。

## 运行流程

### 准备工作

首先需要部署dt-contracts合约，参考[部署教程](https://github.com/ownership-labs/dt-contracts)，并配置DataToken和隐私AI框架的运行环境，参考[SDK使用指南](https://github.com/ownership-labs/DataToken)和[Rosetta使用指南](https://github.com/LatticeX-Foundation/Rosetta)。随后，安装数据服务网格在运行时所需的依赖:

```
$ git clone https://github.com/ownership-labs/Compute-to-Data
$ cd Compute-to-Data
$ pip install -r requirements.txt
```

在测试示例中，Compute-to-Data需与dt-contracts和DataToken在同一目录。我们默认采用私链部署时的四组公钥-私钥对，分别代表系统管理员、数据所有机构1、数据所有机构2和第三方数据科学家：

```
System Key:
0xa2D4eD069A247bcBBeC037FCADd8C3A305b4e409
4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e

Org1 Key:
0x7080b17af4b29F621A5Ef3B1802B2a778Af595d0
5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173

Org2 key:
0xFDEBd75565fE98c1B2659E82181D92B5C6943693
eee795df5de4fc3636abfcfb6d1741665a903efa2b5ded74cea33ca92111b953

3rd-Party key:
0x0148D6F66D4759aC7CcE98673dC9b75974E6bAe4
6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```

### 体验demo