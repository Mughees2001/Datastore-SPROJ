#include "db.h"

Node::Node()
{
    this->prev = NULL;
    this->next = NULL;
    this->d = NULL;
    this->key = "";
}

Node::Node(data *d, std::string key)
{
    this->prev = NULL;
    this->next = NULL;
    this->d = d;
    this->key = key;
}

Node::~Node()
{
    free(this->d);
}

RapidQueue::RapidQueue()
{
    this->head = NULL;
    this->tail = NULL;
    this->size = 0;
    this->map = new std::map<std::string, Node *>();
}

RapidQueue::~RapidQueue()
{
    Node *curr = this->head;
    Node *next = NULL;

    while (curr != NULL)
    {
        next = curr->next;
        delete curr;
        curr = next;
        this->size--;
    }

    delete this->map;
}

void RapidQueue::remove(std::string key)
{
    
}