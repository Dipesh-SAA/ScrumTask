#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ulfius.h>
#include <jansson.h>
#include <uuid/uuid.h>
#include "utils.h"

json_t* validate_calculation_request(json_t *json_body, int require_operation) {
    if (!json_body || !json_is_object(json_body)) {
        return NULL;
    }
    
    json_t *operand1 = json_object_get(json_body, "operand1");
    json_t *operand2 = json_object_get(json_body, "operand2");
    json_t *operation = json_object_get(json_body, "operation");
    
    if (!operand1 || !json_is_number(operand1) ||
        !operand2 || !json_is_number(operand2)) {
        return NULL;
    }
    
    if (require_operation) {
        if (!operation || !json_is_string(operation)) {
            return NULL;
        }
        
        const char *op = json_string_value(operation);
        if (strcmp(op, "add") != 0 && strcmp(op, "subtract") != 0 &&
            strcmp(op, "multiply") != 0 && strcmp(op, "divide") != 0) {
            return NULL;
        }
    }
    
    json_incref(json_body);
    return json_body;
}

void send_error_response(struct _u_response *response, int status, const char *error, const char *message) {
    json_t *error_json = json_object();
    json_object_set_new(error_json, "error", json_string(error));
    json_object_set_new(error_json, "message", json_string(message));
    json_object_set_new(error_json, "statusCode", json_integer(status));
    
    ulfius_set_json_body_response(response, status, error_json);
    json_decref(error_json);
}

double perform_operation(double operand1, double operand2, const char *operation) {
    if (strcmp(operation, "add") == 0) {
        return operand1 + operand2;
    } else if (strcmp(operation, "subtract") == 0) {
        return operand1 - operand2;
    } else if (strcmp(operation, "multiply") == 0) {
        return operand1 * operand2;
    } else if (strcmp(operation, "divide") == 0) {
        if (operand2 == 0) {
            return NAN;
        }
        return operand1 / operand2;
    }
    
    return NAN;
}

char* generate_uuid() {
    uuid_t uuid;
    uuid_generate_random(uuid);
    char *uuid_str = malloc(37);
    uuid_unparse_lower(uuid, uuid_str);
    return uuid_str;
}

char* get_current_timestamp() {
    time_t now = time(NULL);
    struct tm *tm_info = gmtime(&now);
    char *timestamp = malloc(21);
    strftime(timestamp, 21, "%Y-%m-%dT%H:%M:%SZ", tm_info);
    return timestamp;
}