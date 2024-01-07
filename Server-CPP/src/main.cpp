#include <iostream>
#include "db.h"
#include <time.h>

int main(int argc, char *argv[])
{

    if (argc < 3)
    {
        std::cout << "Usage: " << argv[0] << " <ip> <port>" << std::endl;
        return 1;
    }

    // std::cout << argc << std::endl;
    // std::cout << argv[1] << ' ' << argv[2] << std::endl;

    LOG_DEBUG("%d %s %s\n", argc, argv[1], argv[2]);

    RapidQueue *q = new RapidQueue();

    // note start time
    clock_t start = clock();

    for (int i = 0; i < 100000; i++)
    {
        std::string *d = new std::string(std::to_string(i));
        q->put(d, std::to_string(i));
    }

    // note end time
    clock_t end = clock();

    std::string dump = q->getFirstN(10);

    std::cout << dump << std::endl;

    std::cout << "Time taken: " << (double)(end - start) / CLOCKS_PER_SEC << " seconds" << std::endl;

    return 0;
}