#include "client.h"
#include "log.h"

Client::Client(std::string server_host, int server_port)
{
    this->server_host = server_host;
    this->server_port = server_port;
    this->loop = uv_default_loop();
    uv_tcp_init(this->loop, &this->client);
}

Client::~Client()
{
    uv_close((uv_handle_t *)&this->client, NULL);
}

void Client::connect()
{
    struct sockaddr_in dest;
    uv_ip4_addr(this->server_host.c_str(), this->server_port, &dest);
    uv_tcp_connect(&this->connect_req, &this->client, (const struct sockaddr *)&dest, Client::on_connect);
}

void Client::run()
{
    // std::thread input_thread(&Client::input_loop, this);
    std::thread input_thread(std::bind(&Client::input_loop, this));

    // start the event loop
    uv_run(this->loop, UV_RUN_DEFAULT);

    input_thread.join();
}

void Client::on_connect(uv_connect_t *req, int status)
{
    if (status < 0)
    {
        std::cerr << "Error on_connect: " << uv_strerror(status) << std::endl;
        return;
    }

    std::cout << "Connected to server" << std::endl;

    uv_read_start(req->handle, Client::alloc_buffer, Client::on_read);
}

void Client::alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf)
{
    buf->base = (char *)malloc(suggested_size);
    buf->len = suggested_size;
}

void Client::on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf)
{
    if (nread < 0)
    {
        if (nread == UV_EOF)
        {
            std::cout << "Disconnected from server" << std::endl;
        }
        else
        {
            std::cerr << "Error on_read: " << uv_strerror(nread) << std::endl;
        }

        uv_close((uv_handle_t *)client, Client::on_close);
    }
    else if (nread > 0)
    {
        std::cout << "Message: " << buf->base << std::endl;
    }

    if (buf->base)
    {
        LOG_DEBUG("free buf->base %p\n", buf->base);
        free(buf->base);
    }
}

void Client::on_write(uv_write_t *req, int status)
{
    if (status < 0)
    {
        std::cerr << "Error on_write: " << uv_strerror(status) << std::endl;
    }

    if (req->data)
    {
        LOG_DEBUG("free req %p\n", req);
        free(req);
    }
}

void Client::on_close(uv_handle_t *handle)
{
    if (handle->data)
    {
        LOG_DEBUG("free handle %p\n", handle);
        free(handle);
    }
}

void Client::write_data(std::string data)
{
    data += "\n";
    this->buffer = uv_buf_init((char *)data.c_str(), data.size());
    uv_write(&this->write, (uv_stream_t *)&this->client, &this->buffer, 1, Client::on_write);
}

std::string Client::get_command()
{
    std::string command;
    std::cout << "Enter command: ";

    std::getline(std::cin, command); // getline() is used to read a line from a stream (in this case, the standard input stream
    return command;
}

void Client::handle_command(std::string command)
{
    if (command == "exit")
    {
        uv_close((uv_handle_t *)&this->client, NULL);
        exit(0);
    }
    else
    {
        this->write_data(command);
    }
}

void Client::input_loop()
{
    std::string command;
    while (true)
    {
        command = this->get_command();
        this->handle_command(command);
    }
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cout << "Usage: " << argv[0] << " <ip> <port>" << std::endl;
        return 1;
    }

    LOG_DEBUG("%d %s %s\n", argc, argv[1], argv[2]);

    Client *client = new Client(argv[1], atoi(argv[2]));
    client->connect();
    client->run();

    return 0;
}