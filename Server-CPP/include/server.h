#ifndef SERVER_H
#define SERVER_H

#include <iostream>
#include <uv.h>

#include "db.h"

enum Op {
    PUT,
    GET,
};

class ParseReply {
    public:
        int length;
        Op op;
        std::string key;
        std::string value;
        
        // Constructor for PUT
        ParseReply(int length, Op op, std::string key, std::string value) {
            this->length = length;
            this->op = op;
            this->key = key;
            this->value = value;
        }

        // Constructor for GET and DEL
        ParseReply(int length, Op op, std::string key) {
            this->length = length;
            this->op = op;
            this->key = key;
        }
};

class Server
{
    std::string host;
    int port;
    uv_loop_t *loop;
    uv_tcp_t server;
    RapidQueue *db;

    ParseReply *parse_command(std::string command);

public:
    Server(std::string host, int port);
    ~Server();
    void run();
    static void on_new_connection(uv_stream_t *server, int status);
    static void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf);
    static void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf);
    static void on_write(uv_write_t *req, int status);
    static void on_close(uv_handle_t *handle);
    void handle_command(std::string command, uv_stream_t *client);
    bool put(std::string key, std::string value, uv_stream_t *client);
    std::string get(std::string key, uv_stream_t *client);
    bool del(std::string key, uv_stream_t *client);
};

#endif // SERVER_H