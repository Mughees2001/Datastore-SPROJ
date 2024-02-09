/*
 * dev.cpp
 *
 * This file is for development purposes only. It is not part of the final
 * project and is not included in the final build.
 *
 * This file is used to test parts of the implementation.
 *
 */

#include "db.h"

#include <iostream>
#include <string>
#include <time.h>
#include <random>

struct Tuple
{
    int frequency;
    std::string *value;
};

void run_test(std::map<std::string, Tuple> *map, RapidQueue *db)
{
    while (!map->empty())
    {
        // randomly select a key
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, map->size() - 1);
        int index = dis(gen);
        std::map<std::string, Tuple>::iterator it = map->begin();
        std::advance(it, index);

        it->second.frequency--;
        std::cout << "Inserting " << it->first << " with remaining frequency " << it->second.frequency << std::endl;
        db->put(it->second.value, it->first);

        if (it->second.frequency == 0)
        {
            std::cout << "Erasing " << it->first << std::endl;
            map->erase(it);
        }
    }
}

int main(int argc, char *argv[])
{
    int numKeys = 100;           // default value
    int insertionFrequency = 10; // default value

    // Parse command line arguments
    for (int i = 1; i < argc; i++)
    {
        std::string arg = argv[i];
        if (arg == "-n")
        {
            if (i + 1 < argc)
            {
                numKeys = std::stoi(argv[i + 1]);
                i++; // Skip the next argument
            }
            else
            {
                std::cerr << "Error: -n flag requires a value." << std::endl;
                return 1;
            }
        }
        else if (arg == "-d")
        {
            if (i + 1 < argc)
            {
                insertionFrequency = std::stoi(argv[i + 1]);
                i++; // Skip the next argument
            }
            else
            {
                std::cerr << "Error: -d flag requires a value." << std::endl;
                return 1;
            }
        }
        else
        {
            std::cerr << "Error: Unknown flag " << arg << std::endl;
            return 1;
        }
    }

    RapidQueue *db = new RapidQueue();
    std::map<std::string, Tuple> *map = new std::map<std::string, Tuple>();

    for (int i = 0; i < numKeys; i++)
    {
        std::string key = "key" + std::to_string(i);
        std::string *val = new std::string("value" + std::to_string(i));
        Tuple t = {(i + 1) * insertionFrequency, val};
        map->insert(std::pair<std::string, Tuple>(key, t));
    }

    // print the map
    for (std::map<std::string, Tuple>::iterator it = map->begin(); it != map->end(); it++)
    {
        std::cout << it->first << " => " << it->second.frequency << std::endl;
    }

    run_test(map, db);

    return 0;
}
