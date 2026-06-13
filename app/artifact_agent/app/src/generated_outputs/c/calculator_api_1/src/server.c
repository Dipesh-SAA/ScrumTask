#include "server.h"
#include "routes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cjson/cJSON.h>

#define BUFFER_SIZE 1024

void start_server(int port) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
    
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);
    
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
    
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    
    setup_routes();
    
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }
        
        read(new_socket, buffer, BUFFER_SIZE);
        
        // Parse HTTP request
        char method[16], path[256], protocol[16];
        sscanf(buffer, "%s %s %s", method, path, protocol);
        
        // Find request body
        char* request_body = strstr(buffer, "\r\n\r\n");
        if (request_body) {
            request_body += 4;
        }
        
        char* response;
        int status_code;
        handle_request(method, path, request_body, &response, &status_code);
        
        // Send HTTP response
        char http_response[BUFFER_SIZE];
        snprintf(http_response, sizeof(http_response),
                "HTTP/1.1 %d OK\r\n"
                "Content-Type: application/json\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s", 
                status_code, strlen(response), response);
        
        send(new_socket, http_response, strlen(http_response), 0);
        close(new_socket);
        free(response);
    }
}