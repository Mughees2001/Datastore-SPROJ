#ifndef DB_H
#define DB_H

#include "log.h"

#include <iostream>
#include <map>

union data
/**
 * @brief Represents a data structure for storing various types of data.
 *
 * This structure contains an integer, a float, a string, and a void pointer.
 * It can be used to store different types of data in a single object.
 */
{
    int i;
    float f;
    std::string *str;
    void *ptr;
};

/**
 * @brief Represents a node in a data structure.
 */
class Node
{
public:
    Node *prev, *next; /**< Pointers to the previous and next nodes. */
    data *d;           /**< Pointer to the data stored in the node. */
    std::string key;   /**< The key associated with the data. */

    /**
     * @brief Default constructor for Node.
     */
    Node();

    /**
     * @brief Constructor for Node.
     * @param d Pointer to the data to be stored in the node.
     * @param key The key associated with the data.
     */
    Node(data *d, std::string key);

    /**
     * @brief Destructor for Node.
     */
    ~Node();
};

class RapidQueue
{
private:
    Node *head, *tail;
    std::map<std::string, Node *> *map;
    int size;

public:
    RapidQueue();
    ~RapidQueue();

    void remove(std::string key);
};

#endif // DB_H