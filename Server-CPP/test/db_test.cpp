#include "db.h"

#include <iostream>
#include <string>


int main(int argc, char* argv[]) {
    int numKeys = 100; // default value
    int insertionFrequency = 10; // default value

    // Parse command line arguments
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "-n") {
            if (i + 1 < argc) {
                numKeys = std::stoi(argv[i + 1]);
                i++; // Skip the next argument
            } else {
                std::cerr << "Error: -n flag requires a value." << std::endl;
                return 1;
            }
        } else if (arg == "-d") {
            if (i + 1 < argc) {
                insertionFrequency = std::stoi(argv[i + 1]);
                i++; // Skip the next argument
            } else {
                std::cerr << "Error: -d flag requires a value." << std::endl;
                return 1;
            }
        } else {
            std::cerr << "Error: Unknown flag " << arg << std::endl;
            return 1;
        }
    }


    return 0;
}
