#include "server.h"
#include "log.h"


ParseReply *generate_Op(const std::string &s)
{
    std::vector<std::string> *result = new std::vector<std::string>[4]; // max allocation to speed up the process
    std::stringstream ss(s);
    std::string item;

    std::getline(ss, item, ' ');

    ParseReply *reply = new ParseReply;

    // convert to uppercase
    std::transform(item.begin(), item.end(), item.begin(), ::toupper);

    if (item == std::string("PUT"))
    {
        std::getline(ss, item, ' ');
        reply->id = item;
        std::getline(ss, item, ' ');
        reply->key = item;
        std::getline(ss, item, '\n');
        reply->value = new std::string(item);
        reply->op = PUT;
        reply->length = 3;
        return reply;
    }
    else if (item == std::string("GET"))
    {
        std::getline(ss, item, ' ');
        reply->id = item;
        std::getline(ss, item, '\n');
        reply->key = item;
        reply->op = GET;
        reply->length = 2;
        return reply;
    }
    else if (item == std::string("MB_HINT"))
    {
        std::getline(ss, item, ' ');
        reply->id = item;
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = MB_HINT;
        reply->length = 4;
        return reply;
    }
    else if (item == std::string("DISCONNECT"))
    {
        std::getline(ss, item, ' ');
        reply->id = item;
        std::getline(ss, item, ' ');
        reply->host = item;
        std::getline(ss, item, '\n');
        reply->port = std::stoi(item);
        reply->op = DISCONNECT;
        reply->length = 4;
        return reply;
    }
    else
    {
        return reply;
    }
}

std::string extract_id(std::string command)
{
    return command.substr(3, command.length() - 4);
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
            bool res = clients->contains(id);
            if (!res){
                RapidQueue *queue = new RapidQueue();
                uv_mutex_t *lock = new uv_mutex_t;
                uv_mutex_init(lock);
                clients->insert(std::make_pair(id, queue));
                locks->insert(std::make_pair(id, lock));
                std::cout << "New client: " << id << std::endl;
            }
        }
        else
        {
            ParseReply *reply = generate_Op(std::string(buf->base, nread));
            bool find = clients->contains(reply->id);

            if (!find)
            {
                std::cerr << "Client not found" << std::endl;
                return;
            }

            RapidQueue *client_queue = clients->at(reply->id);

            if (reply->op == PUT)
            {
                client_queue->put(reply->value, reply->key);
                char *message = new char[4];
                strcpy(message, "OK\n");
                uv_buf_t wrbuf = uv_buf_init(message, strlen(message));
                uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
                uv_write(req, client, &wrbuf, 1, NULL);
            } 
            else if (reply->op == GET)
            {
                std::string *value = client_queue->get(reply->key);
                char *message = NULL;
                if (value != NULL)
                {
                    message = new char[value->length() + 1];
                    strcpy(message, value->c_str());
                } else {
                    message = new char[5];
                    strcpy(message, "MISS\n");
                } 

                uv_buf_t wrbuf = uv_buf_init(message, strlen(message));
                uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
                uv_write(req, client, &wrbuf, 1, NULL);
            }
            else if (reply->op == MB_HINT){
                // add a function to the event loop
                // uv_work_t *worker = new uv_work_t;
                // worker->data = new std::pair<std::string, int>(reply->host, reply->port);
                // uv_queue_work(loop, worker, mb_hint, mb_hint_done);

                // char *message = new char[4];
                // strcpy(message, "OK\n");
                // uv_buf_t wrbuf = uv_buf_init(message, strlen(message));
                // uv_write_t *req = (uv_write_t *)malloc(sizeof(uv_write_t));
                // uv_write(req, client, &wrbuf, 1, NULL);





            }
            else if (reply->op == DISCONNECT){}
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