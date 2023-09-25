from client import Client
from master import Master, KV
from threading import Thread
from time import time, sleep
from pprint import pprint


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
            sleep(0.001)  # adding a short delay to make the threading undeterministic

    def genValuePairs(self, num_of_keys):
        for i in range(num_of_keys):
            self.kv.append(KV(key=str(i), value=str(i)))
        print(f"Generated {num_of_keys} key-value pairs")

    def Start(self):
        num_keys = 20

        # create 1000 key-value pairs
        self.genValuePairs(num_keys)

        # keep track of update frequency
        kv_dict = {}
        start_time = time()
        # start 1000 threads
        for i in range(num_keys):
            kv_dict[self.kv[i].key] = i
            self.threads.append(
                Thread(
                    target=self.putWrapper, args=(self.kv[i].key, self.kv[i].value, i)
                )
            )

        # start all threads
        for i in range(num_keys):
            self.threads[i].start()

        # wait for all threads to finish
        for i in range(num_keys):
            self.threads[i].join()
        print(f"Time taken to put {num_keys} key-value pairs: {time() - start_time}")

        # use master to get all values in the queue in order
        values_in_master = self.master.currentState()

        # Print all values in master
        pprint(values_in_master)

        # Print all values we inserted
        # sort kv_dict on value
        kv_dict = {k: v for k, v in sorted(kv_dict.items(), key=lambda item: item[1])}
        pprint(kv_dict)

        self.master.exit()

        exit()


if __name__ == "__main__":
    test = Test()
    test.init_master()
    test.init_client()
    test.Start()
