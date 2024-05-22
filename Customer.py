import time

import grpc

import bank_pb2
import bank_pb2_grpc

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub_map = {}

    def getStub(self, branch_id):
        if branch_id in self.stub_map:
            return self.stub_map[branch_id]

        port = 50050 + int(branch_id)  # add the offset for the branch port
        channel = grpc.insecure_channel(f"localhost:{port}")
        self.stub_map[branch_id] = bank_pb2_grpc.BankStub(channel)

        return self.stub_map[branch_id]

    def executeEvents(self):
        bank_responses = []

        for event in self.events:
            response = dict()

            branch_id = int(event["branch"])
            stub = self.getStub(branch_id)

            print("Start request for:", event["interface"], "to branch ", branch_id, end="...", flush=True)

            if event["interface"] == "query":
                bank_response = stub.MsgDelivery(bank_pb2.BankRequest(id=self.id, interface="query"))
                response["interface"] = event["interface"]
                response["branch"] = bank_response.branch
                response["balance"] = bank_response.balance
                bank_responses.append(response)

            elif event["interface"] == "deposit":
                bank_response = stub.MsgDelivery(bank_pb2.BankRequest(id=self.id, interface="deposit", money=event["money"]))
                response["interface"] = event["interface"]
                response["branch"] = bank_response.branch
                response["result"] = bank_response.result
                bank_responses.append(response)

            elif event["interface"] == "withdraw":
                bank_response = stub.MsgDelivery(bank_pb2.BankRequest(id=self.id, interface="withdraw", money=event["money"]))
                response["interface"] = event["interface"]
                response["branch"] = bank_response.branch
                response["result"] = bank_response.result
                bank_responses.append(response)

            print("Completed.")

        return bank_responses
