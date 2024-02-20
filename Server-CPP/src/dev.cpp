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

#include <sstream>
#include <iostream>
#include <string>
#include <time.h>
#include <random>

struct Tuple
{
    int frequency;
    std::string *value;
};


/*
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
        // std::cout << "Inserting " << it->first << " with remaining frequency " << it->second.frequency << std::endl;
        db->put(it->second.value, it->first);

        if (it->second.frequency == 0)
        {
            // std::cout << "Erasing " << it->first << std::endl;
            map->erase(it);
        }
    }
}
*/


enum Op {
    PUT,
    GET,
    MB_HINT,
    DISCONNECT
};



class ParseReply {
    public:
        int length;
        Op op;
        std::string key;
        std::string *value;
        std::string host;
        int port;
        
        ParseReply(){
            this->length = 0;
            this->op = GET;
            this->key = "";
            this->value = NULL;
            this->host = "";
            this->port = 0;
        }

        // Constructor for PUT
        ParseReply(int length, Op op, std::string key, std::string value) {
            this->length = length;
            this->op = op;
            this->key = key;
            this->value = new std::string (value);
        }

        // Constructor for GET and DEL
        ParseReply(int length, Op op, std::string key) {
            this->length = length;
            this->op = op;
            this->key = key;
        }

        // Constructor for MB_HINT and DISCONNECT
        ParseReply(int length, Op op, std::string host, int port) {
            this->length = length;
            this->op = op;
            this->host = host;
            this->port = port;
        }

        friend std::ostream &operator<<(std::ostream &os, const ParseReply &pr) {

            if (pr.op == PUT) {
                os << "PUT " << pr.key << " " << *pr.value;
            } else if (pr.op == GET) {
                os << "GET " << pr.key;
            } else if (pr.op == MB_HINT) {
                os << "MB_HINT " << pr.host << " " << pr.port;
            } else if (pr.op == DISCONNECT) {
                os << "DISCONNECT " << pr.host << " " << pr.port;
            }

            return os;
        }
};

ParseReply *generate_Op(const std::string &s)
{
    std::vector<std::string> *result = new std::vector<std::string>[4]; // max allocation to speed up the process
    std::stringstream ss(s);
    std::string item;

    std::getline(ss, item, ' ');

    ParseReply *reply = new ParseReply;
    if (item == std::string("PUT"))
    {
        std::getline(ss, item, ' ');
        reply->key = item;
        std::getline(ss, item, '\n');
        reply->value = new std::string(item);
        reply->op = PUT;
        reply->length = 3;
        return reply;
    }
    else if (item == std::string("GET"))
    {
        std::getline(ss, item, '\n');
        reply->key = item;
        reply->op = GET;
        reply->length = 2;
        return reply;
    }
    else if (item == std::string("MB_HINT"))
    {
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = MB_HINT;
        reply->length = 4;
        return reply;
    }
    else if (item == std::string("DISCONNECT"))
    {
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = DISCONNECT;
        reply->length = 4;
        return reply;
    }
    else
    {
        return reply;
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

    /*
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
    */

    std::string input;
    std::getline(std::cin, input);
    ParseReply *reply = generate_Op(input);

    std::cout << *reply << std::endl;

    return 0;
}
