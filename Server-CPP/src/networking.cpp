#include "networking.h"

int CreateSocket(int domain, int type, int protocol)
{
    int sock = socket(domain, type, protocol);
    if (sock == -1)
    {
        std::cerr << "Failed to create socket." << std::endl;
        return -1;
    }
    return sock;
}

int BindSocket(int sockfd, const struct sockaddr *addr, socklen_t addrlen)
{
    int bind_result = bind(sockfd, addr, addrlen);
    if (bind_result == -1)
    {
        std::cerr << "Failed to bind socket." << std::endl;
        return -1;
    }
    return 0;
}

int ListenForConnections(int sockfd, int backlog)
{
    int listen_result = listen(sockfd, backlog);
    if (listen_result == -1)
    {
        std::cerr << "Failed to listen for connections." << std::endl;
        return -1;
    }

    struct sockaddr_in addr;
    socklen_t addr_size = sizeof(struct sockaddr_in);
    int res = getsockname(sockfd, (struct sockaddr *)&addr, &addr_size);
    if (res == 0)
    {
        std::cout << "Listening on port " << ntohs(addr.sin_port) << std::endl;
    }
    else
    {
        std::cerr << "Failed to get socket name." << std::endl;
    }

    return 0;
}