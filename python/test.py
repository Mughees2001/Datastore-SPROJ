from client import Client
from master import Master, KV
from threading import Thread
from time import time, sleep
from pprint import pprint
from random import random
from pandas import DataFrame


class Test:
    def __init__(self):
        self.host = "localhost"
        self.port = 12000
        self.master = None
        self.master_thread = None
        self.client = None
        self.threads = []
        self.kv = []

    def init_master(self):
        print("Initializing master")
        self.master = Master(self.host, self.port)
        self.master_thread = Thread(target=self.master.run)
        self.master_thread.start()
        print("Master initialized")

    def init_client(self):
        print("Initializing client")
        self.client = Client(self.host, self.port)
        print("Client initialized")

    def putWrapper(self, key, value, num_iterations):
        for i in range(num_iterations):
            self.client.put(KV(key=key, value=value))
            sleep(0.01)  # adding a short delay to make the threading undeterministic

    def genValuePairs(self, num_of_keys):
        for i in range(num_of_keys):
            self.kv.append(KV(key=str(i), value=str(i)))
        print(f"Generated {num_of_keys} key-value pairs")

    def Start(self):
        num_keys = 100
        # create 1000 key-value pairs
        self.genValuePairs(num_keys)

        # keep track of update frequency
        kv_dict = {}
        start_time = time()

        for i in range(1, num_keys + 1):
            kv_dict[self.kv[i - 1].key] = i

        dict_copy = [(k, v) for k, v in kv_dict.items()]
        while len(dict_copy) > 0:
            # randomly choose to insert a key
            rand = int(random() * len(dict_copy))

            kv: KV = KV(key=dict_copy[rand][0], value=str(dict_copy[rand][1]))
            ret = self.client.put(kv)
            sleep(0.0001)

            # reduce the count of the key
            dict_copy[rand] = (kv.key, int(kv.value) - 1)

            # remove the key if the count is 0
            if dict_copy[rand][1] == 0:
                dict_copy.pop(rand)

        print(f"Time taken to put {num_keys} key-value pairs: {time() - start_time}")

        # use master to get all values in the queue in order
        values_in_master = self.master.inOrderTraversal()
        n_dict = sorted(kv_dict.items(), key=lambda item: item[1], reverse=True)
        values_keys = [item[0] for item in values_in_master]

        differences = []

        print(str.format("{0:10} {1:10}", "Key", "Difference"))
        for i in range(len(n_dict)):
            differences.append(abs(int(values_keys[i]) - int(n_dict[i][0])))
            print(
                str.format(
                    "{0:10} {1:10}",
                    values_keys[i],
                    abs(int(values_keys[i]) - int(n_dict[i][0])),
                )
            )

        print(f"Average difference: {sum(differences) / len(differences)}")
        exit()


if __name__ == "__main__":
    test = Test()
    test.init_master()
    test.init_client()
    test.Start()
