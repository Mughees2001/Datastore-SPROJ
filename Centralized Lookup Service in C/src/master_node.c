#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <openssl/md5.h>
#include <unistd.h> // Include this header for the close function

#define MAX_SERVERS 10 // Maximum number of registered servers
#define PORT 8000 // Maximum number of registered servers
#define MAX_KEY_VALUE_LENGTH 512


typedef struct {
    char ip[20]; // IP address of the server
    int port;    // Port number of the server
    unsigned int hash;
} ServerNode;

ServerNode servers[MAX_SERVERS];
int num_servers = 0;

// Hash function to calculate hash value
unsigned int hash(const char *key) {
    unsigned char digest[MD5_DIGEST_LENGTH];
    MD5((unsigned char*)key, strlen(key), digest);

    uint32_t hash_value = ((uint32_t)digest[3] << 24) | ((uint32_t)digest[2] << 16) |
                          ((uint32_t)digest[1] << 8) | (uint32_t)digest[0];

    return hash_value % (1 << 16);
}

// Register a new server with the master node
void register_server(const char *ip, int port) {
    if (num_servers < MAX_SERVERS) {
        // Convert the port number to a string
        char port_str[6];  // Enough space for 5 digits + null terminator
        sprintf(port_str, "%d", port);
        // Calculate the maximum length of the concatenated string
        int max_length = strlen(ip) + strlen(port_str) + 2; // IP + ":" + Port + '\0'
        // Allocate memory for the concatenated string
        char *ip_port_str = (char *)malloc(max_length * sizeof(char));
        snprintf(ip_port_str, max_length, "%s:%s", ip, port_str);
        unsigned int hash_val = hash(ip_port_str);
        free(ip_port_str);
        strcpy(servers[num_servers].ip, ip);
        servers[num_servers].port = port;
        servers[num_servers].hash = hash_val; // Store the hash value
        num_servers++;
    } else {
        printf("Maximum number of servers reached\n");
    }
}
unsigned int clockwise_distance(unsigned int hash1, unsigned int hash2, unsigned int max_hash) {
    if (hash1 <= hash2) {
        return hash2 - hash1;
    } else {
        return (max_hash - hash1) + hash2 + 1;
    }
}


ServerNode find_server(const char *key) {
    unsigned int key_hash = hash(key);
    unsigned int max_hash = 1 << 16; // Maximum hash value for 16-bit representation
    ServerNode next_server = servers[0]; // Initialize to the first server

    // Initialize the minimum clockwise distance to a large value
    unsigned int min_distance = max_hash;

    for (int i = 0; i < num_servers; ++i) {
        unsigned int server_hash = servers[i].hash;
        unsigned int distance = clockwise_distance(key_hash, server_hash, max_hash);
        if (distance < min_distance) {
            min_distance = distance;
            next_server = servers[i];
        }
    }

    return next_server;
}


int main(int argc, char *argv[]) {
    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, 5) == -1) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }
    printf("Master node listening on port %d\n", PORT);

    while (1) {
        client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
        if (client_socket == -1) {
            perror("Accept failed");
            continue;
        }
        char request[512];
        int bytes_received = recv(client_socket, request, sizeof(request), 0);
        if (bytes_received <= 0) {
            continue; // No more data or connection closed
        }
        request[bytes_received] = '\0';  // Ensure null-termination
        if (strncmp(request, "REGISTER", 8) == 0) {
            char ip[20];
            int port;
            sscanf(request, "REGISTER %s %d", ip, &port);
            register_server(ip, port);
            printf("Registered server: %s:%d with hash:%d\n", ip, port,servers[num_servers-1].hash);
            send(client_socket, "Registered", 10, 0);
        }  else if (strncmp(request, "PUT", 3) == 0 || strncmp(request, "GET", 3) == 0)   {
            // Parse the key from the request
            char key[MAX_KEY_VALUE_LENGTH];
            if(strncmp(request, "PUT", 3) == 0 ){
                sscanf(request, "PUT %s", key);
            } else if (strncmp(request, "GET", 3) == 0){
                sscanf(request, "GET %s", key);
            }
            // Determine the server that will handle the key
            printf("Key:%s with Hash:%d \n",key,hash(key));
            ServerNode server = find_server(key);
            char response[1024];
            snprintf(response, sizeof(response), "IP:%s,PORT:%d", server.ip, server.port);
            send(client_socket, response, strlen(response), 0);
        }
        else {
            send(client_socket, "Invalid command", 15, 0);
        }
    }

    return 0;
}
