import time
from concurrent import futures
from threading import Lock

import json
import sys

import grpc
import bank_pb2
import bank_pb2_grpc


class Branch(bank_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # write set
        self.track_write_set = {}
        # lock
        self.lock = Lock()
        # iterate the processID of the branches
        for branch in self.branches:
            channel = grpc.insecure_channel(f"localhost:{branch}")
            stub = bank_pb2_grpc.BankStub(channel)
            self.stubList.append(stub)

    # RPC method to handle Customer and Branch requests
    def MsgDelivery(self, request, context):

        lock = None
        response = None

        if request.id in self.track_write_set:
            lock = self.lock.acquire()

        if request.interface == "query":
            # print("Query received from customer ", request.id)
            response = bank_pb2.BankResponse(result="success", balance=self.balance, branch=self.id)

        elif request.interface == "deposit":
            self.balance = self.balance + request.money
            # propogate Deposit to other branches asynchronously
            Helper.propogate_async("Propogate_Deposit", request.id, request.money, self.stubList)

        elif request.interface == "withdraw":
            self.balance = self.balance - request.money
            # propogate Withdraw to other branches asynchronously
            Helper.propogate_async("Propogate_Withdraw", request.id, request.money, self.stubList)

        elif request.interface == "Propogate_Deposit":
            # create propogation delay with sleep
            # print("Received propagate: ")
            Helper.track_write_and_acquire_lock(self, request.id, self.lock)
            time.sleep(2)
            self.balance = self.balance + request.money
            Helper.untrack_write_and_release_lock(self, request.id, self.lock)

        elif request.interface == "Propogate_Withdraw":
            # create propogation delay with sleep
            Helper.track_write_and_acquire_lock(self, request.id, self.lock)
            time.sleep(2)
            self.balance = self.balance - request.money
            Helper.untrack_write_and_release_lock(self, request.id, self.lock)

        response = bank_pb2.BankResponse(result="success", balance=self.balance, branch=self.id)

        if lock is not None:
            self.lock.release()
            lock = None

        return response


class Helper:

    def callback(future):
        print("Callback: ", future.result())

    def propogate_async(interface, custID, money, stub_list):

        # propogate event to other branches
        for stub in stub_list:
            # async RPC request to other branch
            response_future = stub.MsgDelivery.future(bank_pb2.BankRequest(id=custID, interface=interface, money=money))
            response_future.add_done_callback(Helper.callback)

    def track_write_and_acquire_lock(branchObj, id, lock):
        print("updating write_set for id: ",id, branchObj.track_write_set)
        branchObj.track_write_set[id] = True
        print("updated write_set for id: ",id, branchObj.track_write_set)
        lock.acquire()

    def untrack_write_and_release_lock(branchObj, id, lock):
        if id in branchObj.track_write_set:
            del branchObj.track_write_set[id]
            lock.release()


    def serve(id, balance, branches):
        port = 50050 + id  # add the offset for the branch port
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        bank_pb2_grpc.add_BankServicer_to_server(Branch(id, balance, branches), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print(f"Server started. Listening on port {port}")
        server.wait_for_termination()


# parse arguments
parameters = json.loads(str(sys.argv[1]).replace("\'", "\""))

Helper.serve(int(parameters["id"]), int(parameters["balance"]), parameters["branches"])
