#ifndef ROUTES_H
#define ROUTES_H

#include <stdbool.h>

void setup_routes();
void handle_request(const char* method, const char* path, const char* request_body, char** response, int* status_code);

#endif