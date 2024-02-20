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
};

std::vector<std::string> *split(std::string s, char delim){
    
    std::vector<std::string> *result = new std::vector<std::string>;
    std::stringstream ss(s);
    std::string item;

    std::cout << "String to parse " << s << std::endl;
    
    int count = 0;
    while (std::getline(ss, item, ' ')){
        result->push_back(item);
        std::cout << ++count << std::endl;
    }
    return result;
}

ParseReply *generate_Op(const std::string &s){
    std::vector<std::string> *result = split(s, ' ');

    std::string res = result->at(0);
    if (res == (std::string)"PUT"){
        return new ParseReply(3, PUT, result->at(1), result->at(2));
    } else if (res == (std::string)"MB_HINT"){
        return new ParseReply(4, MB_HINT, result->at(1), std::stoi(result->at(2)));
    } else if (res == (std::string)"DISCONNECT"){
        return new ParseReply(4, DISCONNECT, result->at(1), std::stoi(result->at(2)));
    } 
    else {
        return new ParseReply(2, GET, result->at(1));
    }
}

ParseReply *parse_command(std::string command)
{
    std::string op = command.substr(0, 3);

    if (op == "PUT")
    {
        // find second space
        int space = command.find(" ", 4);

        // key is from 4 to space - 4
        std::string key = command.substr(4, space - 4);

        // value is from space + 1 to end - 1
        std::string value = command.substr(space + 1, command.length() - space - 1);

        return new ParseReply(3, PUT, key, value);
    }
    else
    {
        // find first space
        int space = command.find(" ");

        // key is from 4 to space - 4
        std::string key = command.substr(4, space - 4);

        return new ParseReply(2, GET, key);
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
    std::vector<std::string> *tokens = split(input, ' ');

    for(int i = 0; i < tokens->size(); i++){
        std::cout << tokens->at(i) << std::endl;
    }

    return 0;
}
