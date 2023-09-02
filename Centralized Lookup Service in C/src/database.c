#include "database.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_KEY_VALUES 5000
#define MAX_KEY_LENGTH 64
#define MAX_VALUE_LENGTH 256

void init_database(Database *db) {
    db->data = malloc(sizeof(KeyValuePair) * MAX_KEY_VALUES); // Initialize with a fixed size
    db->size = MAX_KEY_VALUES;
    for (size_t i = 0; i < db->size; i++) {
        db->data[i].key[0] = '\0'; // Mark all slots as empty
        db->data[i].value[0] = '\0';
    }
}

int put(Database *db, const char *key, const char *value) {
    // Find an empty slot in the database or replace the value if there exists a key...
    for (size_t i = 0; i < db->size; i++) {
        if (strcmp(db->data[i].key, key) == 0 || db->data[i].key[0] == '\0') {
            strncpy(db->data[i].key, key, MAX_KEY_LENGTH - 1);
            db->data[i].key[MAX_KEY_LENGTH - 1] = '\0';  // Ensure null-termination
            strncpy(db->data[i].value, value, MAX_VALUE_LENGTH - 1);
            db->data[i].value[MAX_VALUE_LENGTH - 1] = '\0';  // Ensure null-termination
            printf("Put: Key '%s' Value '%s'\n", key, value);
            return 1;
        }
    }
    printf("Database is full\n");
    return 0;
}

const char* get(Database *db, const char *key) {
    for (size_t i = 0; i < db->size; i++) {
        if (strcmp(db->data[i].key, key) == 0) {
            printf("Get: Key '%s' Value '%s'\n", key, db->data[i].value);
            return db->data[i].value;
        }
    }

    printf("Key '%s' not found\n", key);
    return NULL;
}
