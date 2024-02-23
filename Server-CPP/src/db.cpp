#include "db.h"

Node::Node()
{
    this->prev = NULL;
    this->next = NULL;
    this->d = NULL;
    this->key = "";
}

Node::Node(std::string *d, std::string key)
{
    this->prev = NULL;
    this->next = NULL;
    this->d = d;
    this->key = key;
}

// Node::~Node()
// {
//     free(this->d);
// }

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
    // get the node from the map
    Node *node = this->map->at(key);

    if (node == NULL)
    {
        return;
    }

    if (node->prev == NULL)
    {
        // node is the head
        this->head = node->next;
    }
    else
    {
        node->prev->next = node->next;
    }

    if (node->next == NULL)
    {
        // node is the tail
        this->tail = node->prev;
    }
    else
    {
        node->next->prev = node->prev;
    }

    // remove the node from the map
    this->map->erase(key);

    // delete the node
    // node->~Node();

    // decrement the size
    this->size--;
}

bool RapidQueue::put(std::string *d, std::string key)
{
    // check if the key already exists
    if (this->map->count(key) > 0)
    {
        // remove the existing node
        this->remove(key);
    }

    // create a new node
    Node *node = new Node(d, key);

    // add the node to the map
    this->map->insert(std::pair<std::string, Node *>(key, node));

    if (this->head == NULL)
    {
        // the queue is empty
        this->head = node;
        this->tail = node;
    }
    else
    {
        // the queue is not empty
        this->tail->next = node;
        node->prev = this->tail;
        this->tail = node;
    }

    // increment the size
    this->size++;

    return true;
}

std::string *RapidQueue::get(std::string key)
{
    bool exists = this->map->contains(key);

    if (!exists)
    {
        return NULL;
    }

    // get the node from the map
    Node *node = this->map->at(key);

    if (node == NULL)
    {
        return NULL;
    }

    return node->d;
}

// std::string RapidQueue::getValueString(const data &value)
// {
//     // if (value.str != nullptr)
//     // {
//     //     return *value.str;
//     // }
//     // else if (value.ptr != nullptr)
//     // {
//     //     // Assuming the pointer points to a string
//     //     return *static_cast<std::string *>(value.ptr);
//     // }
//     // else
//     // {
//     //     // Handle other types as needed (int, float)
//     //     if (value.i != 0)
//     //     {
//     //         std::cout << "Returning int" << std::endl;
//     //         return std::to_string(value.i);
//     //     }
//     //     else if (value.f != 0.0f)
//     //     {
//     //         return std::to_string(value.f);
//     //     }
//     //     else
//     //     {
//     //         return "Unknown Type";
//     //     }
//     // }

//     return "";
// }

std::string RapidQueue::getFirstN(int n)
{
    std::string result = "";

    Node *curr = this->head;
    int i = 0;

    while (curr != NULL && i < n)
    {
        result += curr->key + ": " + *curr->d + "\n";
        curr = curr->next;
        i++;
    }

    return result;
}

std::string RapidQueue::startMigration()
{
    std::string result = "";

    result = getFirstN(this->size / 2);

    return result;
}