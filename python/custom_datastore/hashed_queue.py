from typing import Optional, List

class QueueNode():
    def __init__(self, key : str, value : str):
        self.key = key
        self.value = value
        self.next : Optional[QueueNode] = None
        self.prev : Optional[QueueNode] = None
        

class HashTableNode():
    def __init__(self, node : QueueNode):
        self.queue_node : QueueNode = node
        self.next : Optional[HashTableNode] = None


"""
    Summary:
        The goal here is to create a queue where insert and delete options are O(1)
        The easy way to insert and delete in O(1) is to have a doubly linked list
        However, the problem arises when we want to look up keys. The update API for our datastore needs to have a O(1) (or close enough) time.
        The goal here is to find the node that contains the data, while ensuring that we can traverse the queue and hash tables when we want to create a list

"""
class HashQueue():
    def __init__(self, max_size):
        self.head = None
        self.tail = None
        self.size = 0
        self.max_size = max_size
        self.hash_table = [None for i in range(max_size)]
        self.previous_insertion : Optional[HashTableNode] = None

    def insert(self, key : str, value : str):

        # calculate the hash of the value
        hash_val = hash(key) % self.max_size
        
        q_node = QueueNode(key, value)
        h_node = HashTableNode(q_node)

        # inserting if the table is empty
        if self.size == 0:
            self.hash_table[hash_val] = h_node
            
            pass
        
        
        

    