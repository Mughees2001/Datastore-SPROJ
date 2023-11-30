#include <sys/socket.h>
#include <netinet/in.h>
#include <iostream>

/**
 * @brief Create a new communication endpoint (socket) of the specified domain, type, and protocol.
 *
 * @param domain The domain of the socket (e.g. AF_INET for IPv4).
 * @param type The type of the socket (e.g. SOCK_STREAM for TCP).
 * @param protocol The protocol to be used with the socket (e.g. IPPROTO_TCP for TCP).
 * @return int The file descriptor for the new socket, or -1 if an error occurred.
 */
int CreateSocket(int domain, int type, int protocol);

/**
 * Initiates a connection on a socket.
 *
 * @param sockfd The socket file descriptor.
 * @param addr A pointer to the sockaddr structure containing the destination address.
 * @param addrlen The length of the sockaddr structure.
 * @return 0 on success, -1 on failure.
 */
int ConnectClient(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

/**
 * @brief Binds a socket to a specific address and port.
 *
 * @param sockfd The socket file descriptor.
 * @param addr The address to bind to.
 * @param addrlen The length of the address structure.
 * @return int Returns 0 on success, -1 on failure.
 */
int BindSocket(int sockfd, const struct sockaddr *addr, socklen_t addrlen);

/**
 * @brief Listen for incoming connections on a socket.
 *
 * @param sockfd The socket file descriptor to listen on.
 * @param backlog The maximum length to which the queue of pending connections may grow.
 * @return 0 on success, -1 on error.
 */
int ListenForConnections(int sockfd, int backlog);

/**
 * @brief Accept a new connection on a socket.
 *
 * @param sockfd The socket file descriptor to listen on.
 * @param addr   A pointer to a sockaddr structure that will hold the address of the connecting entity.
 * @param addrlen A pointer to a socklen_t structure that will hold the length of the sockaddr structure.
 *
 * @return On success, returns a non-negative integer that is a descriptor for the accepted socket. On error, -1 is returned.
 */
int AcceptConnection(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
