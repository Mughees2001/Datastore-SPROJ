#include "server.h"
#include "log.h"

/*
// Server::Server(std::string host, int port)
// {
//     this->host = host;
//     this->port = port;
//     this->loop = uv_default_loop();
//     this->clients = new std::map<std::string, RapidQueue *>;
// }

// Server::~Server()
// {
//     uv_loop_close(this->loop);
// }

// ParseReply *Server::parse_command(std::string command)
// {
//     std::string op = command.substr(0, 3);

//     if (op == "PUT")
//     {
//         // find second space
//         int space = command.find(" ", 4);

//         // key is from 4 to space - 4
//         std::string key = command.substr(4, space - 4);

//         // value is from space + 1 to end
//         std::string value = command.substr(space + 1);

//         return new ParseReply(3, PUT, key, value);
//     }
//     else
//     {
//         // find first space
//         int space = command.find(" ");

//         // key is from 4 to space - 4
//         std::string key = command.substr(4, space - 4);

//         return new ParseReply(2, GET, key);
//     }
// }

// void Server::run()
// {
//     struct sockaddr_in addr;
//     uv_ip4_addr(this->host.c_str(), this->port, &addr);
//     uv_tcp_init(this->loop, &this->server);
//     uv_tcp_bind(&this->server, (const struct sockaddr *)&addr, 0);
//     int r = uv_listen((uv_stream_t *)&this->server, 128, on_new_connection);
//     if (r)
//     {
//         std::cerr << "Listen error " << uv_strerror(r) << std::endl;
//         return;
//     }
//     std::cout << "Listening on " << this->host << ":" << this->port << std::endl;
//     uv_run(this->loop, UV_RUN_DEFAULT);
// }

// void Server::on_new_connection(uv_stream_t *server, int status)
// {
//     if (status < 0)
//     {
//         std::cerr << "New connection error " << uv_strerror(status) << std::endl;
//         return;
//     }
//     uv_tcp_t *client = (uv_tcp_t *)malloc(sizeof(uv_tcp_t));

//     uv_tcp_init(uv_default_loop(), client);
//     if (uv_accept(server, (uv_stream_t *)client) == 0)
//     {
//         uv_read_start((uv_stream_t *)client, Server::alloc_buffer, Server::on_read);
//         struct sockaddr_storage peername;
//         int namelen = sizeof(peername);
//         if (uv_tcp_getpeername(client, (struct sockaddr *)&peername, &namelen) == 0)
//         {
//             if (peername.ss_family == AF_INET)
//             {
//                 struct sockaddr_in *srcaddr = (struct sockaddr_in *)&peername;
//                 char ip[INET_ADDRSTRLEN];
//                 uv_inet_ntop(AF_INET, &(srcaddr->sin_addr), ip, sizeof(ip));
//                 std::cout << "New connection from " << ip << ":" << ntohs(srcaddr->sin_port) << std::endl;
//             }
//             else if (peername.ss_family == AF_INET6)
//             {
//                 struct sockaddr_in6 *srcaddr = (struct sockaddr_in6 *)&peername;
//                 char ip[INET6_ADDRSTRLEN];
//                 uv_inet_ntop(AF_INET6, &(srcaddr->sin6_addr), ip, sizeof(ip));
//                 std::cout << "New connection from " << ip << ":" << ntohs(srcaddr->sin6_port) << std::endl;
//             }
//         }
//     }
//     else
//     {
//         uv_close((uv_handle_t *)client, NULL);
//     }

// }

// void Server::alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf)
// {
//     buf->base = (char *)malloc(suggested_size);
//     buf->len = suggested_size;
// }

// void Server::on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf)
// {
//     if (nread > 0)
//     {
//         std::cout << "Read: " << buf->base << std::endl;
//         uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
//         uv_buf_t wrbuf = uv_buf_init(buf->base, nread);
//         uv_write(req, client, &wrbuf, 1, Server::on_write);
//         return;
//     }
//     if (nread < 0)
//     {
//         if (nread != UV_EOF)
//         {
//             std::cerr << "Read error " << uv_err_name(nread) << std::endl;
//         }
//         uv_close((uv_handle_t *)client, this->on_close);
//     }
//     free(buf->base);
// }

// void Server::on_write(uv_write_t *req, int status)
// {
//     if (status)
//     {
//         std::cerr << "Write error " << uv_strerror(status) << std::endl;
//     }
//     free(req);
// }

// void Server::on_close(uv_handle_t *handle)
// {
//     free(handle);
// }

// void Server::handle_command(std::string command, uv_stream_t *client)
// {
//     ParseReply *reply = parse_command(command);

//     if (reply->op == PUT)
//     {
//         std::cout << "PUT " << reply->key << " " << reply->value << std::endl;
//     }

//     if (reply->op == GET)
//     {
//         std::cout << "GET " << reply->key << std::endl;
//     }
// }
*/

std::vector<std::string> *split(const std::string &s, char delim)
{
    std::vector<std::string> *result = new std::vector<std::string>;
    std::stringstream ss(s);
    std::string item;

    while (std::getline(ss, item, delim))
    {
        result->push_back(item);
    }
    return result;
}

ParseReply *generate_Op(const std::string &s)
{
    std::vector<std::string> *result = new std::vector<std::string>[4]; // max allocation to speed up the process
    std::stringstream ss(s);
    std::string item;

    // first token
    std::getline(ss, item, ' ');

    ParseReply *reply = new ParseReply;
    if (item == std::string("PUT"))
    {
        std::getline(ss, item, ' ');
        reply->key = item;
        std::getline(ss, item, '\n');
        reply->value = new std::string(item);
        reply->op = PUT;
        return reply;
    }
    else if (item == std::string("GET"))
    {
        std::getline(ss, item, '\n');
        reply->key = item;
        reply->op = GET;
        return reply;
    }
    else if (item == std::string("MB_HINT"))
    {
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = MB_HINT;
        return reply;
    }
    else if (item == std::string("DISCONNECT"))
    {
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = DISCONNECT;
        return reply;
    }
    else
    {
        return reply;
    }
}

ParseReply *parse_command(std::string command)
{
    std::string op = command.substr(0, 3);

    if (op == "PUT")
    {
        // find second space
        int space = command.find(" ", 4);

        // key is from 4 to space - 4
        std::string key = command.substr(4, space - 4);

        // value is from space + 1 to end - 1
        std::string value = command.substr(space + 1, command.length() - space - 1);

        return new ParseReply(3, PUT, key, value);
    }
    else
    {
        // find first space
        int space = command.find(" ");

        // key is from 4 to space - 4
        std::string key = command.substr(4, space - 4);

        return new ParseReply(2, GET, key);
    }
}

std::string extract_id(std::string command)
{
    return command.substr(2, command.length() - 2);
}

void on_read(uv_stream_t *client, ssize_t nread, const uv_buf_t *buf)
{
    if (nread > 0)
    {
        // std::cout << "Read: " << buf->base << std::endl;
        // uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
        // uv_buf_t wrbuf = uv_buf_init(buf->base, nread);
        // uv_write(req, client, &wrbuf, 1, NULL);

        // check the first two characters
        if (buf->base[0] == 'I' && buf->base[1] == 'D')
        {
            char *message = new char[4];
            strcpy(message, "OK\n");
            uv_buf_t wrbuf = uv_buf_init(message, strlen(message));
            uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
            uv_write(req, client, &wrbuf, 1, NULL);

            std::string id = extract_id(buf->base);

            // check if the id is in the map
            // bool res = clients->contains(id);
            // if (!res){

            // }
        }
        else
        {
            ParseReply *reply = parse_command(buf->base);
            if (reply->op == PUT)
            {
                std::cout << "PUT key=" << reply->key << " value=" << reply->value;
            }

            if (reply->op == GET)
            {
                std::cout << "GET " << reply->key;
            }
        }

        return;
    }
    if (nread < 0)
    {
        if (nread != UV_EOF)
        {
            std::cerr << "Read error " << uv_err_name(nread) << std::endl;
        }
        uv_close((uv_handle_t *)client, NULL);
    }
    free(buf->base);
}

void alloc_buffer(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf)
{
    buf->base = (char *)malloc(suggested_size);
    buf->len = suggested_size;
}

void on_new_connection(uv_stream_t *server, int status)
{
    if (status < 0)
    {
        std::cerr << "New connection error " << uv_strerror(status) << std::endl;
        return;
    }

    uv_tcp_t *client = (uv_tcp_t *)malloc(sizeof(uv_tcp_t));
    uv_tcp_init(loop, client);

    if (uv_accept(server, (uv_stream_t *)client) == 0)
    {
        uv_read_start((uv_stream_t *)client, alloc_buffer, on_read);
    }
    else
    {
        uv_close((uv_handle_t *)client, NULL);
    }

    // send a message to the client
    char *message = new char[4];
    strcpy(message, "ID\n");
    uv_buf_t wrbuf = uv_buf_init(message, strlen(message));
    uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
    uv_write(req, (uv_stream_t *)client, &wrbuf, 1, NULL);
}

int main(int argc, char *argv[])
{

    if (argc < 3)
    {
        std::cout << "Usage: " << argv[0] << " <ip> <port>" << std::endl;
        return 1;
    }

    LOG_DEBUG("%d %s %s\n", argc, argv[1], argv[2]);

    // Server *server = new Server(argv[1], atoi(argv[2]));
    // server->run();

    loop = uv_default_loop();
    struct sockaddr_in addr;
    uv_tcp_init(loop, &server);
    uv_ip4_addr(argv[1], atoi(argv[2]), &addr);
    uv_tcp_bind(&server, (const struct sockaddr *)&addr, 0);
    int r = uv_listen((uv_stream_t *)&server, 128, on_new_connection);

    if (r)
    {
        std::cerr << "Listen error " << uv_strerror(r) << std::endl;
        return 1;
    }

    std::cout << "Listening on " << argv[1] << ":" << argv[2] << std::endl;

    clients = new std::map<std::string, RapidQueue *>;
    locks = new std::map<std::string, uv_mutex_t *>;

    uv_run(loop, UV_RUN_DEFAULT);

    return 0;
}