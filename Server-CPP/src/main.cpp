#include <iostream>
#include "db.h"

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

    return 0;
}