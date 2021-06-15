# Compute-to-Data

[中文版](./README_CN.md)

## Overview

This project implements a on-premise data sandbox for serving private computation of sensitive data. Third-party scientists can execute codes remotely and get results on data they cannot see. The data grid will automatically verify the data service terms for its owner. The whole process of data sharing and utilization is traceable and auditable.

We provide `dsb` and `dt_cli` toolkits for data owners and scientists. The `dsb` is a Flask-based service deployment tool for data assets, allowing data owners to quickly define computing services and verify external job requests according to agreements. The `dt_cli` is a client tool for datatoken services and remote execution.

## Play With It

### user story

Consider the joint risk management scenario, a third-party fintech company C provides model solutions for two banks A and B. Sensitive customer data are stored in their private databases. Only when data privacy is guaranteed and external operations are auditable, band A and B are allowed to receive and authorize the third party's model to perform on-premise computation. By using the DataToken SDK, data owners can trade the computation rights of their private data, and thus data becomes assets in the marketplace.

### run tests

We provide [dt-examples](https://github.com/ownership-labs/dt-examples) for testing. Required config files, datasets, asset metadatas and federated models are all included. For each on-premise computation, a seperate folder will be created for storing running resources and logs. Each job will have a corresponding folder like `tests/job_id/`, in which datasets, models and parameters will be fetched to the disk automatically. This simply simulates a private computation sandbox.
