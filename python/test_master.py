from master import Master, KV
from time import time
from typing import List
from random import random
from sys import argv
from log import logger
from pprint import pprint


class MasterOnly:
    def __init__(self, num_keys, key_frequency=1):
        self.host = "localhost"
        self.port = 12000
        self.master = Master(self.host, self.port)
        self.num_keys = num_keys
        self.keys: List[KV] = []
        self.key_frequency = key_frequency

    def generate_kv(self):
        for i in range(self.num_keys):
            self.keys.append(KV(key=str(i), value=str(i)))
        print(f"Generated {self.num_keys} key-value pairs")

    def run(self):
        # generate keys
        self.generate_kv()

        # keep track of update frequency
        kv_dict = {}
        start_time = time()

        for i in range(1, self.num_keys + 1):
            kv_dict[self.keys[i - 1].key] = i * self.key_frequency

        dict_copy = [(k, v) for k, v in kv_dict.items()]
        while len(dict_copy) > 0:
            rand = int(random() * len(dict_copy))

            kv: KV = KV(key=dict_copy[rand][0], value=str(dict_copy[rand][1]))
            self.master.put(kv)

            # reduce the count of the key
            dict_copy[rand] = (kv.key, int(kv.value) - 1)

            # remove the key if the count is 0
            if dict_copy[rand][1] == 0:
                dict_copy.pop(rand)

        print(
            f"Time taken to put {self.num_keys} key-value pairs: {time() - start_time}"
        )

        # use master to get all values in the queue in order
        values_in_master = self.master.inOrderTraversal()
        n_dict = sorted(kv_dict.items(), key=lambda item: item[1], reverse=True)
        values_keys = [item[0] for item in values_in_master]

        differences = []

        for i in range(len(n_dict)):
            differences.append(abs(int(values_keys[i]) - int(n_dict[i][0])))

        with open(f"./log/{self.key_frequency}/log_{self.num_keys}.txt", "w") as f:
            f.write("Values in master\n")
            f.write(str(values_keys))
            f.write("\n")
            f.write("True values\n")
            f.write(str(n_dict))
            f.write("\n")
            f.write("Differences\n")
            f.write(str(differences))
            f.write("\n")

        # print(f"Average difference: {sum(differences) / len(differences)}")
        exit()


if __name__ == "__main__":
    if len(argv) == 2:
        test = MasterOnly(int(argv[1]))
    elif len(argv) == 3:
        # logger.warning(f"Key freqency {argv[2]} provided")
        test = MasterOnly(int(argv[1]), int(argv[2]))
    else:
        logger.warning("No argument provided, using default value of 100")
        test = MasterOnly(100)
    test.run()
