#ifndef HANDLERS_H
#define HANDLERS_H

#include <stdbool.h>
#include "calculator.h"

void handle_create_calculation(const char* request_body, char** response, int* status_code);

#endif