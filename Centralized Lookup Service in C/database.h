#include <stdio.h>
#include <stdlib.h>

#ifndef DATABASE_H
#define DATABASE_H

#define PORT 8888
#define MAX_KEY_LENGTH 64
#define MAX_VALUE_LENGTH 256

typedef struct {
    char key[MAX_KEY_LENGTH];
    char value[MAX_VALUE_LENGTH];
} KeyValuePair;

typedef struct {
    KeyValuePair *data;
    size_t size;
} Database;

void init_database(Database *db);
int put(Database *db, const char *key, const char *value);
const char* get(Database *db, const char *key);

#endif /* DATABASE_H */
