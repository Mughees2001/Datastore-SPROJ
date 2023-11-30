#include "server.h"

int main()
{
    std::cout << "Hello World!" << std::endl;
    int socket = CreateSocket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket == -1)
    {
        std::cerr << "Failed to create socket." << std::endl;
        return 1;
    }
    std::cout << "Created Socket" << std::endl;

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(9000);
    addr.sin_addr.s_addr = INADDR_ANY;
    int bind_result = BindSocket(socket, (struct sockaddr *)&addr, sizeof(addr));
    if (bind_result == -1)
    {
        std::cerr << "Failed to bind socket." << std::endl;
        return 2;
    }
    std::cout << "Bound Socket" << std::endl;

    while (1)
    {
    }

    return 0;
}