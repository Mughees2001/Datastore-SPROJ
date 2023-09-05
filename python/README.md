# Python Implementation of the DataStore

This folder contains the Python implementation of a datastore. The idea here is to test out the datastore implementation in Python before implementing it in C.

## Progress

### 3rd September 2023

A very basic version of the data store has been implemented. It is a single server that a client can connect to. It is completely in-memory and uses the Python dictionary to store data.

The operations implemented are:

1. PUT
2. GET
3. DELETE

To test the implementation, we can run the following commands in two separate terminals:

Terminal 1:

```bash
python3 master.py <host> <port>
```

Terminal 2:

```bash
python3 client.py <server host> <server port>
```

#### TO DO

1. Implement a suitable testing suite that can run multiple thousand requests per second and check to see if the data store is working as expected.
2. Implement a migrate API that can migrate the contents of a server to another server.
3. Figure out a larger picture for coordinating multiple servers and clients.
