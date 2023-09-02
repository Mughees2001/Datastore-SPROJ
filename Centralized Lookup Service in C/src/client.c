#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h> // Include this header for the close function


#define MASTER_NODE_IP "127.0.0.1" // Change this to the IP of the master node
#define MASTER_NODE_PORT 8000 // Change this to the port of the master node

#define MAX_KEY_VALUE_LENGTH 512

int main() {

    while (1) {

        int client_socket;
        struct sockaddr_in master_addr;
        client_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (client_socket == -1) {
            perror("Socket creation failed");
            exit(EXIT_FAILURE);
        }

        //Connecting to Master Node
        memset(&master_addr, 0, sizeof(master_addr));
        master_addr.sin_family = AF_INET;
        master_addr.sin_port = htons(MASTER_NODE_PORT);
        master_addr.sin_addr.s_addr = inet_addr(MASTER_NODE_IP);

        if (connect(client_socket, (struct sockaddr *)&master_addr, sizeof(master_addr)) == -1) {
            perror("Connection failed");
            exit(EXIT_FAILURE);
        }
        //Sending the query to Master node for get or put which will reply us that which server contains the keys
        char command[MAX_KEY_VALUE_LENGTH];
        char response[MAX_KEY_VALUE_LENGTH];
        //Applying checks to see whether the command is valid or not..
        int valid_command = 0;
        while (!valid_command) {
            printf("Enter command (PUT key value / GET key): ");
            fgets(command, sizeof(command), stdin);
            command[strlen(command) - 1] = '\0'; // Remove the newline character

            if (strncmp(command, "PUT ", 4) == 0 && strlen(command) > 4) {
                // Check if there are enough tokens after splitting
                char key[MAX_KEY_VALUE_LENGTH];
                char value[MAX_KEY_VALUE_LENGTH];
                if (sscanf(command, "PUT %s %s", key, value) == 2) {
                    // Valid PUT command format
                    valid_command = 1;
                } else {
                    printf("Invalid PUT command format. Please use 'PUT key value' format.\n");
                }
            } else if (strncmp(command, "GET ", 4) == 0 && strlen(command) > 4) {
                // Valid GET command format
                valid_command = 1;
            } else {
                printf("Invalid command format. Please use either 'PUT key value' or 'GET key' format.\n");
            }
        }


        if (send(client_socket, command, strlen(command), 0) == -1) {
            perror("Send failed");
            exit(EXIT_FAILURE);
        }
        int bytes_received = recv(client_socket, response, sizeof(response), 0);
        if (bytes_received == -1) {
            perror("Receive failed");
            exit(EXIT_FAILURE);
        }

        response[bytes_received] = '\0';
        printf("Response: %s\n", response);
        close(client_socket);

        // Parse the response to get the server IP and port
        char server_ip[20];
        int server_port;

        sscanf(response, "IP:%[^,],PORT:%d", server_ip, &server_port);
        if (strcmp(server_ip, "localhost") == 0) {
            // Replace "localhost" with the actual IP address (127.0.0.1 in this case)
            strncpy(server_ip, "127.0.0.1", sizeof(server_ip) - 1);
            server_ip[sizeof(server_ip) - 1] = '\0'; // Ensure null-termination
        }
        // Contacting the actual server in hash ring for PUT and GET commands..(This will serve to the client)
        printf("Contacting %s:%d\n", server_ip,server_port);
        int server_socket;
        struct sockaddr_in server_addr;

        server_socket = socket(AF_INET, SOCK_STREAM, 0);
        if (server_socket == -1) {
            perror("Socket creation failed");
            exit(EXIT_FAILURE);
        }

        memset(&server_addr, 0, sizeof(server_addr));
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(server_port);
        server_addr.sin_addr.s_addr = inet_addr(server_ip);

        if (connect(server_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
            perror("Connection to server failed");
            exit(EXIT_FAILURE);
        }

        // Now you can send the PUT or GET command to the server
        if (send(server_socket, command, strlen(command), 0) == -1) {
            perror("Send failed");
            exit(EXIT_FAILURE);
        }

        char server_response[MAX_KEY_VALUE_LENGTH];
        bytes_received = recv(server_socket, server_response, sizeof(server_response), 0);
        if (bytes_received == -1) {
            perror("Receive failed");
            exit(EXIT_FAILURE);
        }

        server_response[bytes_received] = '\0';
        printf("Server response: %s\n", server_response);
        close(server_socket);


    }

    return 0;
}
