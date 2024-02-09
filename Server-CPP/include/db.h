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
    std::string *d;    /**< Pointer to the data stored in the node. */
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
    Node(std::string *d, std::string key);

    // /**
    //  * @brief Destructor for Node.
    //  */
    // ~Node();
};

/**
 * @brief Represents a rapid queue data structure.
 *
 * The RapidQueue class provides functionality to store and retrieve data in a queue-like manner.
 * It supports operations like putting data, getting data, removing data, and starting migration.
 */
class RapidQueue
{
private:
    Node *head, *tail;
    std::map<std::string, Node *> *map;
    int size;

    // std::string getValueString(const data &value);

public:
    /**
     * @brief Represents a RapidQueue object.
     *
     * This class is responsible for managing a queue of elements in a rapid manner.
     * It provides methods for adding and removing elements from the queue.
     */
    RapidQueue();
    /**
     * @brief Destructor for the RapidQueue class.
     */
    ~RapidQueue();

    /**
     * @brief Removes a key-value pair from the database.
     *
     * @param key The key of the pair to be removed.
     */
    void remove(std::string key);

    /**
     * @brief Inserts a data object into the database with the specified key.
     *
     * @param d A pointer to the data object to be inserted.
     * @param key The key associated with the data object.
     * @return true if the data object was successfully inserted, false otherwise.
     */
    bool put(std::string *d, std::string key);

    /**
     * @brief Retrieves the data associated with the given key.
     *
     * @param key The key to retrieve the data for.
     * @return The data union associated with the key.
     */
    std::string *get(std::string key);

    /**
     * @brief Retrieves the first N elements from the database.
     *
     * @param n The number of elements to retrieve.
     * @return A string containing the first N elements.
     */
    std::string getFirstN(int n);

    /**
     * @brief Returns the least frequently updated n/2 key-value pairs.
     *
     * This function retrieves the least frequently updated n/2 key-value pairs from the data store.
     * The pairs are selected based on the frequency of updates, with the least frequently updated pairs being returned.
     *
     * @return A `std::string` containing the least frequently updated n/2 key-value pairs.
     */
    std::string startMigration();
};

#endif // DB_H