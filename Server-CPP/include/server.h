#ifndef SERVER_H
#define SERVER_H

#include <sstream>
#include <iostream>
#include <uv.h>
#include <map>
#include <vector>
#include <cstring>

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
        std::string id;
        std::string key;
        std::string *value;
        std::string host;
        int port;
        
        ParseReply(){
            this->length = 0;
            this->op = GET;
            this->id = "";
            this->key = "";
            this->value = NULL;
            this->host = "";
            this->port = 0;
        }

        // Constructor for PUT
        ParseReply(int length, Op op, std::string id, std::string key, std::string value) {
            this->length = length;
            this->op = op;
            this->id = id;
            this->key = key;
            this->value = new std::string (value);
        }

        // Constructor for GET and DEL
        ParseReply(int length, Op op, std::string id, std::string key) {
            this->length = length;
            this->op = op;
            this->id = id;
            this->key = key;
        }

        // Constructor for MB_HINT and DISCONNECT
        ParseReply(int length, Op op, std::string id, std::string host, int port) {
            this->length = length;
            this->op = op;
            this->id = id;
            this->host = host;
            this->port = port;
        }

        friend std::ostream &operator<<(std::ostream &os, const ParseReply &pr) {

            if (pr.op == PUT) {
                os << "PUT " << pr.key << " " << *pr.value << " " << pr.id;
            } else if (pr.op == GET) {
                os << "GET " << pr.key << " " << pr.id;
            } else if (pr.op == MB_HINT) {
                os << "MB_HINT " << pr.host << " " << pr.port << " " << pr.id;
            } else if (pr.op == DISCONNECT) {
                os << "DISCONNECT " << pr.host << " " << pr.port << " " << pr.id;
            }

            return os;
        }
};



static uv_loop_t *loop;
static uv_tcp_t server;

std::map<std::string, RapidQueue *> *clients;
std::map<std::string,  uv_mutex_t *> *locks;

static void on_new_connection(uv_stream_t *server, int status);
static void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf);
static void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf);

#endif // SERVER_H