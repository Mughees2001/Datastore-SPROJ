from typing import Dict,List
import pprint



class MultipleHashQueue:
    def __init__(self,initQueueSize):
        self.initQueueSize = initQueueSize
        self.Queues = [HashQueue(self.initQueueSize)]

    def fixQueue(self,queueNumber):
        if (self.Queues[queueNumber].needNewQueue()):
            (lastKey,lastValue) = (self.Queues[queueNumber].tail.key,self.Queues[queueNumber].tail.value)
            try:
                self.Queues[queueNumber+1].putQueue(lastKey,lastValue)
            except:
                self.Queues.append(HashQueue(self.initQueueSize * 1<<len(self.Queues))) # Initial Queue Size * 2()
                self.Queues[queueNumber+1].putQueue(lastKey,lastValue) #Inserting the Last key value of previous queue into the head of new Queue.
            self.Queues[queueNumber].deleteQueue(lastKey)
        elif self.Queues[queueNumber].currentSize == 0:
            self.Queues.pop()
      
    def put(self,key,value):
        self.Queues[0].putQueue(key,value)
        for i in range(len(self.Queues)):
            if i!=0:
                self.Queues[i].deleteQueue(key) #In case the key already existed in any other Queue
            self.fixQueue(i)
    
    def delete(self,key):
        for i in range(len(self.Queues)):
            if self.Queues[i].deleteQueue(key) is True:
                return True
        return False
        
    def get(self,key):
        for i in range(len(self.Queues)):
            value = self.Queues[i].getQueue(key)
            if value != "MISS":
                return value
        return "MISS"
    
    def currentState(self):
        dictState = {}
        for i in range(len(self.Queues)):
            temp = "Queue"+str(i+1)
            dictState[temp] = self.Queues[i].currentStateQueue()
        return dictState
    
class Node:
    def __init__(self, key,value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None
    
class HashQueue:
    def __init__(self,size):
        self.map: Dict[str, Node] = {}
        self.head = None
        self.tail = None
        self.size = size
        self.currentSize = 0
    
    def needNewQueue(self):
        if self.size < self.currentSize:
            return True
        return False
        
    def getQueue(self,key):
        if key in self.map:
            return self.map[key].value
        else:
            return "MISS"
        
    def putQueue(self,key,value):
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
        self.currentSize += 1
    
    def deleteQueue(self,key):
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
            self.currentSize -= 1
            del node
            del self.map[key]
        return True
        
    def currentStateQueue(self):
        node = self.head
        retList = []
        while node:
            retList.append((node.key,node.value))
            node = node.next
        state = {}
        state['Size Allowed'] = self.size
        state['Current Size'] = self.currentSize
        state['Items'] = retList
        return state