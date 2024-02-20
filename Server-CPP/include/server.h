#ifndef SERVER_H
#define SERVER_H

#include <sstream>
#include <iostream>
#include <uv.h>
#include <map>

#include "db.h"

enum Op {
    PUT,
    GET,
    MB_HINT,
    DISCONNECT
};


std::vector<std::string> *split(const std::string &s, char delim);


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
};

// class Server
// {
//     std::string host;
//     int port;
//     uv_loop_t *loop;
//     uv_tcp_t server;
//     std::map<std::string, RapidQueue *> *clients;
//
//     ParseReply *parse_command(std::string command);
//
// public:
//     Server(std::string host, int port);
//     ~Server();
//     void run();
//     static void on_new_connection(uv_stream_t *server, int status);
//     static void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf);
//     void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf);
//     void on_write(uv_write_t *req, int status);
//     void on_close(uv_handle_t *handle);
//     void handle_command(std::string command, uv_stream_t *client);
//     bool put(std::string key, std::string *value, uv_stream_t *client);
//     std::string *get(std::string key, uv_stream_t *client);
//     bool del(std::string key, uv_stream_t *client);
// };

static uv_loop_t *loop;
static uv_tcp_t server;

std::map<std::string, RapidQueue *> *clients;
std::map<std::string,  uv_mutex_t *> *locks;

static void on_new_connection(uv_stream_t *server, int status);
static void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf);
static void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf);

#endif // SERVER_H