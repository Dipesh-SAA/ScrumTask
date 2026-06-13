#include "calculator.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <uuid/uuid.h>

bool calculate(const CalculationRequest* request, CalculationResponse* response, ErrorResponse* error) {
    uuid_t uuid;
    uuid_generate_random(uuid);
    char uuid_str[37];
    uuid_unparse_lower(uuid, uuid_str);
    
    time_t now = time(NULL);
    char* time_str = ctime(&now);
    time_str[strlen(time_str)-1] = '\0'; // Remove newline
    
    response->id = strdup(uuid_str);
    response->operand1 = request->operand1;
    response->operand2 = request->operand2;
    response->operation = request->operation;
    response->createdAt = strdup(time_str);
    
    switch (request->operation) {
        case OP_ADD:
            response->result = request->operand1 + request->operand2;
            break;
        case OP_SUBTRACT:
            response->result = request->operand1 - request->operand2;
            break;
        case OP_MULTIPLY:
            response->result = request->operand1 * request->operand2;
            break;
        case OP_DIVIDE:
            if (request->operand2 == 0) {
                error->error = strdup("division_by_zero");
                error->message = strdup("Cannot divide by zero");
                error->statusCode = 400;
                return false;
            }
            response->result = request->operand1 / request->operand2;
            break;
        default:
            error->error = strdup("invalid_operation");
            error->message = strdup("Invalid operation type");
            error->statusCode = 400;
            return false;
    }
    
    return true;
}