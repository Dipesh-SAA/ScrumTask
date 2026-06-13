#include "server.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    int port = 8080;
    if (argc > 1) {
        port = atoi(argv[1]);
    }
    
    printf("Starting calculator API server on port %d\n", port);
    start_server(port);
    
    return 0;
}