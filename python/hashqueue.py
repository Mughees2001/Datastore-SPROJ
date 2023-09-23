from typing import Dict


class Node:
    def __init__(self, key,value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
    
class HashQueue:
    def __init__(self):
        self.map: Dict[str, Node] = {}
        self.head = None
        self.tail = None
        self.size = 0
        self.NumOfHotKeys = 2

    def get(self,key):
        if key in self.map:
            self.delete(key)
            self.insertAtHead(key)
            return self.map[key].value
        else:
            return "MISS"
        
    def put(self,key,value):
        if key in self.map:
            node = self.map[key]
            node.value = value
            self.delete(key)
            self.insertAtHead(key)
        else:
            node = Node(key,value)
            self.map[key] = node
            self.insertAtHead(key)
    
    def insertAtHead(self,key):
        node = self.map[key]
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1
    
    def delete(self,key):
        if key not in self.map:
            return False
        else:
            node = self.map[key]
            if node.prev is None:
                self.head = node.next
            else:
                node.prev.next = node.next
            if node.next is None:
                self.tail = node.prev
            else:
                node.next.prev = node.prev
            self.size -= 1
            del node
        return True
        
    def hotKeys(self,limit):
        node = self.head
        retList = []
        while node and limit > 0 and limit <= self.size:
            retList.append(node.key)
            node = node.next
            limit -= 1
        return retList
    
    def currentState(self):
        node = self.head
        retList = []
        while node:
            retList.append((node.key,node.value))
            node = node.next
        state = {}
        state['HotKeysPick'] = self.NumOfHotKeys
        state['Size'] = self.size
        state['HotKeys'] = self.hotKeys(self.size//3)
        state['Datastore'] = retList
        return state
