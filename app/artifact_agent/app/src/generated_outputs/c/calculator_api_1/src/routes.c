#include "routes.h"
#include "handlers.h"
#include <string.h>

void setup_routes() {
    // Route setup would be handled by the server implementation
}

void handle_request(const char* method, const char* path, const char* request_body, char** response, int* status_code) {
    if (strcmp(method, "POST") == 0 && strcmp(path, "/calculations") == 0) {
        handle_create_calculation(request_body, response, status_code);
    } else {
        *status_code = 404;
        cJSON* error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "not_found");
        cJSON_AddStringToObject(error_response, "message", "Endpoint not found");
        cJSON_AddNumberToObject(error_response, "statusCode", 404);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
    }
}