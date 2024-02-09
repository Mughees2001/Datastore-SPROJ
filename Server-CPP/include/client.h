#ifndef CLIENT_H
#define CLIENT_H

#include <uv.h>
#include <iostream>
#include <thread>
#include <functional>

class Client
{
    std::string server_host;
    int server_port;
    uv_loop_t *loop;
    uv_tcp_t client;
    uv_connect_t connect_req;
    uv_write_t write;
    uv_buf_t buffer;

    // channel for 


public:
    Client(std::string server_host, int server_port);
    ~Client();
    void connect();
    static void on_connect(uv_connect_t *req, int status);
    static void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf);
    static void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf);
    static void on_write(uv_write_t *req, int status);
    static void on_close(uv_handle_t *handle);

    void write_data(std::string data);
    std::string get_command();

    void handle_command(std::string command);
    void input_loop();
    void run();
};

#endif // CLIENT_H