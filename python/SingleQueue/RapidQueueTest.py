from lib.RapidQueue import RapidQueue
from time import time


class RapidQueueTest:
    def __init__(self, num: int):
        self.rapid_queue = RapidQueue()
        self.test_keys = [f"key{i}" for i in range(num)]
        self.test_values = [f"value{i}".encode() for i in range(num)]

    def run(self):
        for index, key in enumerate(self.test_keys):
            self.rapid_queue.put(key, self.test_values[index])

        print(f"Insertion of {len(self.test_keys)} unique keys completed")

    def __str__(self):
        return str(self.rapid_queue)


def main():
    tests = RapidQueueTest(100000)
    start_time = time()
    tests.run()
    print(f"Time taken: {time() - start_time}")

    pass


if __name__ == "__main__":
    main()
