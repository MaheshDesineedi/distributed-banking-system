# Client Centric Consistency for Distributed Banking Application

![gRPC](https://img.shields.io/badge/gRPC-4285F4?logo=grpc&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Multi-threading](https://img.shields.io/badge/Multi--threading-007ACC?logo=windows-terminal&logoColor=white)
![Consistency](https://img.shields.io/badge/Consistency-FF6F00?logo=databricks&logoColor=white)
![Distributed Transactions](https://img.shields.io/badge/Distributed%20Transactions-4DB33D?logo=redis&logoColor=white)


## Overview

Develop a distributed data store that ensures "read-your-writes" consistency. Customer transactions at one location should reflect across all locations, maintaining updated balances for each customer. The communication between different processes is done using gRPC.

## Key Highlights
- Ensures `read-your-writes` consistency for customer updates across different branches.
- Supports distributed transactions across multiple branches.
- Propagates updates asynchronously between branches.
- Supports basic banking operations: Query, Deposit, and Withdraw.
- Places customer requests on hold if a previous write operation is still being propagated.
- Defines Protobuf request messages containing parameters (id, interface, money).
- Utilizes gRPC for efficient and reliable communication with well defined Protocol Buffers.
- Provides a clear setup and installation process.
- Ensures all processes and gRPC channels are gracefully terminated using signal handlers.
- Designed to handle multiple branches and customer requests.
- Utilizes sleep methods to simulate propagation delays and ensure consistent updates.
- Tracks and logs customer requests and branch operations.
- Parses input customer JSON and sends events to branches concurrently.
- Tracks customer write requests using `track_write_set` dictionary and locks the transaction if previous write is pending for a customer.
- Includes thorough testing with various input scenarios.
- Validated with `input_big.json` test case with an automated checker script for correct transaction execution and consistency.

## Customer and Branch Interactions
![image](https://github.com/MaheshDesineedi/banking-client-consistency/blob/main/C2BDesgin.png)

## Requirements

- Python 3.7+
- Pip 9.0.1+
- Git
- Linux/Unix (Ubuntu 20.04, MacOS)
- 8GB+ RAM

## Installation

Step-by-step instructions on how to set up and run the project.

### Clone the repository
```bash

git clone https://github.com/MaheshDesineedi/banking-client-consistency

# Change to the project directory
cd banking-client-consistency

```

### Install and initiate a virtual environment:
```bash
python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### Install grpcio and grpcio-tools which also includes protocol buffer compiler protoc:
```bash
python -m pip install grpcio grpcio-tools
```

###	Execute Instructions:
```bash

# Place the test JSON file in test folder. See src/test/input_big.json

# Open a new terminal and create branch servers using below command:
python run_branch.py <path_to_test_json_file>

# Open a new terminal and create customer processes using below command:
python run_customer.py <path_to_test_json_file>
```

### Results
Observe the output JSON (/output/output.json) file. Each item represents the type of transaction (balance query/deposit/withdraw) and its result/balance.





