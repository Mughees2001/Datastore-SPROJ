from typing import Dict, Any, Optional


class Node:
    """
    The Node class contains a key and a value. The key is used to
    identify the node in the queue. The value is the value of the
    node.
    """

    def __init__(self, key: str, value: bytes):
        self.key: str = key
        self.value: bytes = value
        self.next: Node = None
        self.prev: Node = None


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
        self.head: Node = None
        self.tail: Node = None

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
        except KeyError as e:
            print(e)

    def put(self, key: str, value: bytes) -> bool:
        """
        This function will search for the node in the queue.
        If it already exists, we will remove it from the queue
        Then we will insert a new node at the tail.
        """
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
            self.tail.next = node
            self.tail = node

        self.store[key] = node

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

    def startMigration(self) -> str:
        # traverse through the queue and prepare a dump
        # for each node we traverse, we remove it from the queue

        dump: str = str()
        traverse: Node = self.head
        old: Node = None

        while traverse:
            dump += f"{traverse.key} {traverse.value.decode()};"
            old = traverse
            traverse = traverse.next
            old.next = None
            old.prev = None

        return dump

    def __str__(self):
        """
        This function will return the string representation of the
        queue.
        """
        node = self.head
        string = ""

        while node is not None:
            string += f"{node.key} -> "
            node = node.next

        return string
