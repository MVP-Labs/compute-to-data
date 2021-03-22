
[中文版](./demo_CN.md)

### Prerequisites

First you need to deploy the dt-contracts contract, refer to [Deployment Tutorial](https://github.com/ownership-labs/dt-contracts), and configure the DataToken environment and the private AI framework, refer to [SDK Guide](https://github.com/ownership-labs/DataToken) and [Rosetta Guide](https://github.com/LatticeX-Foundation/Rosetta). Then, you can install the dependencies using the commands:

```
$ git clone https://github.com/ownership-labs/Compute-to-Data
$ cd Compute-to-Data
$ pip install -r requirements.txt
```

In this demo, you need to put the Compute-to-Data, dt-contracts and DataToken repos in the same directory. By default, we use four pre-defined key pairs for the system administrator, bank A, bank B and third-party C.

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

### Play With It

#### System Administrator

The system administrator configures the federated model and its metadata in ./samples/op, and then publishs the model on-chain as the trusted operator:
```
$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ python client/dt-cli.py system org --name 'org1' --desc 'test_org1' --address 0x7080b17af4b29F621A5Ef3B1802B2a778Af595d0 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
```

Bank A, bank B, and third-party C are registered as asset providers:
```
$ python client/dt-cli.py system org --name 'org2' --desc 'test_org2' --address 0xFDEBd75565fE98c1B2659E82181D92B5C6943693 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
$ python client/dt-cli.py system org --name '3rd-party' --desc 'test_3rd' --address  0x0148D6F66D4759aC7CcE98673dC9b75974E6bAe4 --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
$ python client/dt-cli.py system op --attr_file ./samples/op/rtt_op_attr.json --private_key 4472aa5d4e2efe297784a3d44d840c9652cdb7663e22dedd920958bf6edfaf7e
```

#### Band A and B

Banks put their private data in ./samples/data/, simulating the on-premise storage. Then, metadatas need to be defined and published using asset schema, pre-configured in ./samples/ddo/. Specifically, the identifier of trusted operator is included in the metadata, declaring how data can be used:
```
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org1_feature_attr.json --private_key 5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org1_label_attr.json --private_key 5c25a2fb9b5427bbe8b68b4ddc0655ae7621f87a147a489b1337ca166bca0173
$ python client/dt-cli.py asset dt --attr_file ./samples/ddo/org2_feature_attr.json --private_key eee795df5de4fc3636abfcfb6d1741665a903efa2b5ded74cea33ca92111b953
```

You can see the datatoken identifiers in the console. After that, running configurations need to be filled in ./samples/config, including private key, contract keeper, service endpoint and data storage. Finally, open two terminals and run the rtt_tracer for service deployment:
```
$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ export CONFIG_FILE=./samples/config/org1_config.ini
$ python rtt_tracer/daemon.py

$ export PYTHONPATH=$PYTHONPATH:../dt-asset:/../dt-web3:/../DataToken:/../Compute-to-Data
$ export CONFIG_FILE=./samples/config/org2_config.ini
$ python rtt_tracer/daemon.py
```

#### Third-party C

The third-party C defines its algorithm metadata, with the computing workflow and related fulfillments inside it, applied on banks' data assets. Similarily, publish it on-chain and get composable data token:
```
python client/dt-cli.py asset cdt --attr_file ./samples/ddo/3rd_algo_attr.json --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```

Tasks can be created for data collaborations. Run the remote computing jobs on A and B:
```
python client/dt-cli.py job init --name 'test' --desc 'test_task' --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
python client/dt-cli.py job exec --task_id 1 --cdt 'dt:ownership:34940ace7bdacfff97f4c5dd348f523119fdf1c82aa3ec2bf99149e88499a961' --private_key 6bba7694acf53fd8d02120263e6e5aaacbab4b623f4a401ac835c9d8ec54e122
```

The output can be viewed in tests/{job_id}/outputs/rtt_log.txt. We will provide the querying function for getting the remote status.

#### Regulator

Regulatory parties can trace the whole lifecycle of data sharing and utilization:
```
python client/dt-cli.py tracer dfs --prefix_path "dt:ownership:34940ace7bdacfff97f4c5dd348f523119fdf1c82aa3ec2bf99149e88499a961"
```