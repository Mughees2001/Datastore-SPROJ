#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include "database.h"
#include <pthread.h>
#include <unistd.h> // Include this header for the close function


#define MASTER_IP "127.0.0.1"
#define MASTER_PORT 8000
#define MAX_KEY_VALUE_LENGTH 512

struct ThreadArgs {
    Database *db;
    int client_socket;
};


void register_to_master(const char *ip, int port) {
    int client_socket;
    struct sockaddr_in server_addr;

    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(MASTER_PORT);
    server_addr.sin_addr.s_addr = inet_addr(MASTER_IP);

    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connection to master node failed");
        exit(EXIT_FAILURE);
    }

    char register_request[512];
    snprintf(register_request, sizeof(register_request), "REGISTER %s %d", ip, port);
    send(client_socket, register_request, strlen(register_request), 0);

    char response[512];
    int bytes_received = recv(client_socket, response, sizeof(response), 0);
    if (bytes_received == -1) {
        perror("Receive failed");
        exit(EXIT_FAILURE);
    }
    response[bytes_received] = '\0';
    printf("Master node response: %s\n", response);
    close(client_socket);

}


void *handle_client(void *arg) {
    struct ThreadArgs *args = (struct ThreadArgs *)arg;
    Database *db = args->db;
    int client_socket = args->client_socket;
    free(args);

   
    char request[512];
    int bytes_received = recv(client_socket, request, sizeof(request), 0);
    if (bytes_received <= 0) {
        close(client_socket); // No more data or connection closed
    }
    request[bytes_received] = '\0';  // Ensure null-termination
    if (strncmp(request, "PUT", 3) == 0) {
        char key[MAX_KEY_LENGTH];
        char value[MAX_VALUE_LENGTH];
        char response[512];
        sscanf(request, "PUT %s %s", key, value);  // Notice the comma separator
        int success = put(db, key, value);
        if (success) {
            snprintf(response, sizeof(response), "Put Success");
        } else {
            snprintf(response, sizeof(response), "Put Failed");
        }
        send(client_socket, response, strlen(response), 0);
    } else if (strncmp(request, "GET", 3) == 0) {
        char key[MAX_KEY_LENGTH];
        sscanf(request, "GET %s", key);
        const char *value = get(db, key);
        if (value != NULL) {
            send(client_socket, value, strlen(value), 0);
        } else {
            const char *not_found = "Key not found";
            send(client_socket, not_found, strlen(not_found), 0);
        }
    } else {
        const char *invalid_command = "Invalid command";
        send(client_socket, invalid_command, strlen(invalid_command), 0);
    }
    close(client_socket);

    // Close the client socket and detach the thread
    pthread_detach(pthread_self());
    return NULL;
}



int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <server_ip> <server_port>\n", argv[0]);
        return 1;
    }

    const char *server_ip = argv[1];
    int server_port = atoi(argv[2]);
    //Intializing database
    Database db;
    init_database(&db);

    register_to_master(server_ip, server_port);

    
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
    server_addr.sin_port = htons(server_port);

    if (bind(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, 5) == -1) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }
    printf("Server listening on port %d\n", server_port);


    //Handling incoming connections from client and creating a seperate thread for the client..
    while (1) {
        client_socket = accept(server_socket, (struct sockaddr *)&client_addr, &client_len);
        if (client_socket == -1) {
            perror("Accept failed");
            continue;
        }
        struct ThreadArgs *args = malloc(sizeof(struct ThreadArgs));
        args->db = &db;
        args->client_socket = client_socket;
        // Create a new thread to handle the client
        pthread_t tid;

        if (pthread_create(&tid, NULL, handle_client, args) != 0) {
            perror("Thread creation failed");
            free(args);
            continue;
        }
         // Detach the thread to allow it to clean up itself
        pthread_detach(tid);
    }
    
    free(db.data); // Free allocated memory

    return 0;
}
