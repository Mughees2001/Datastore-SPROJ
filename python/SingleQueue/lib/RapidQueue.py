import time
from typing import Any, Dict, Optional


class Node:
    """
    The Node class contains a key and a value. The key is used to
    identify the node in the queue. The value is the value of the
    node.
    """

    def __init__(self, key: str, value: bytes):
        self.key: str = key
        self.value: bytes = value
        self.next: Optional[Node] = None
        self.prev: Optional[Node] = None


class RapidQueue:
    """
    The RapidQueue class contains a map that contains the location
    of all nodes in a queue. This can be used to find any key in
    O(1) complexity.

    We will keep track of the head and tail of the queue. The head
    contains the least recently used node. The tail contains the
    most recently used node.
    """

    def __init__(self):
        self.store: Dict[str, Node] = dict()
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length: int = 0

    def remove(self, key: str):
        """
        This function will remove a node from the queue.
        """
        try:
            k = self.store[key]  # fetching the node

            if k.prev:
                k.prev.next = (
                    k.next
                )  # setting the next node of the previous node to the next node of the current node

            if k.next:
                k.next.prev = (
                    k.prev
                )  # setting the previous node of the next node to the previous node of the current node

            del self.store[key]  # deleting the node from the store
            self.length -= 1  # decrementing the length of the queue
        except KeyError as e:
            print(e)

    def put(self, key: str, value: bytes) -> bool:
        """
        This function will search for the node in the queue.
        If it already exists, we will remove it from the queue
        Then we will insert a new node at the tail.
        """
        start_time: Any = time.time()
        # remove spaces from the right
        # value = value.rstrip()
        node = Node(key, value)

        if key in self.store:
            self.remove(key)

        """
        Queue can be in two states. Either it has a head and a tail
        or it is empty. If it is empty, we will set the head and tail
        to the new node. If it is not empty, we will set the next node
        of the tail to the new node and set the previous node of the
        new node to the tail. Then we will set the tail to the new node.
        """
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            if self.tail:
                self.tail.next = node
            self.tail = node

        self.store[key] = node
        self.length += 1

        # add time in nano seconds to file
        end_time: Any = time.time()
        time_taken: float = end_time - start_time
        with open("put_times.txt", "a") as f:
            f.write(f"{time_taken}\n")
        return True

    def get(self, key: str) -> Optional[bytes]:
        """
        This function returns the value of the key if it exists.
        """
        try:
            node = self.store[key]
            return node.value
        except KeyError as e:
            print(e)

        return None

    def getFirstN(self, n: int) -> str:
        """
        This function removes the first n nodes from the queue and
        returns them.

        Args:
            n (int): Number of elements to be removed

        Returns:
            str: A string containing the keys and values of the removed nodes
        """
        buff: str = str()
        traverse: Optional[Node] = self.head
        old: Node
        while traverse is not None and n > 0:
            buff += f"{traverse.key} {traverse.value.decode()};"
            old = traverse
            traverse = traverse.next
            old.next = None
            old.prev = None
            n -= 1
            self.length -= 1
            if self.length == 0:
                self.head = None
                self.tail = None
            elif self.length == 1:
                self.head = traverse
                self.tail = traverse
            else:
                self.head = traverse
                if traverse:
                    traverse.prev = None

        return buff

    def startMigration(self):
        """
        Retrieves the first half of the items in the queue and returns them as a string.
        """

        buffer: str = self.getFirstN(int(self.length / 2))
        return buffer

    def __str__(self):
        """
        This function will return the string representation of the
        queue.
        """
        node = self.head
        string = ""

        while node is not None:
            string += f"{node.key}: {node.value} -> "
            node = node.next

        return string
