#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "routes.h"
#include "models.h"
#include "calculator.h"
#include "cJSON.h"

void setup_routes() {
    // Route setup would be implemented here
    // In a real implementation, this would integrate with a web server
}

void handle_create_calculation(const char *request_body, char **response, int *status_code) {
    cJSON *json = cJSON_Parse(request_body);
    if (!json) {
        *status_code = 400;
        cJSON *error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "Bad Request");
        cJSON_AddStringToObject(error_response, "message", "Invalid JSON");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        return;
    }
    
    cJSON *operand1 = cJSON_GetObjectItemCaseSensitive(json, "operand1");
    cJSON *operand2 = cJSON_GetObjectItemCaseSensitive(json, "operand2");
    cJSON *operation = cJSON_GetObjectItemCaseSensitive(json, "operation");
    
    if (!operand1 || !operand2 || !operation) {
        *status_code = 400;
        cJSON *error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "Bad Request");
        cJSON_AddStringToObject(error_response, "message", "Missing required fields");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        cJSON_Delete(json);
        return;
    }
    
    if (!cJSON_IsNumber(operand1) || !cJSON_IsNumber(operand2) || !cJSON_IsString(operation)) {
        *status_code = 400;
        cJSON *error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "Bad Request");
        cJSON_AddStringToObject(error_response, "message", "Invalid field types");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        cJSON_Delete(json);
        return;
    }
    
    const char *op = operation->valuestring;
    if (strcmp(op, "add") != 0 && strcmp(op, "subtract") != 0 && 
        strcmp(op, "multiply") != 0 && strcmp(op, "divide") != 0) {
        *status_code = 400;
        cJSON *error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "Bad Request");
        cJSON_AddStringToObject(error_response, "message", "Invalid operation");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        cJSON_Delete(json);
        return;
    }
    
    double op1 = operand1->valuedouble;
    double op2 = operand2->valuedouble;
    double result;
    
    if (strcmp(op, "add") == 0) {
        result = add(op1, op2);
    } else if (strcmp(op, "subtract") == 0) {
        result = subtract(op1, op2);
    } else if (strcmp(op, "multiply") == 0) {
        result = multiply(op1, op2);
    } else if (strcmp(op, "divide") == 0) {
        if (op2 == 0) {
            *status_code = 400;
            cJSON *error_response = cJSON_CreateObject();
            cJSON_AddStringToObject(error_response, "error", "Bad Request");
            cJSON_AddStringToObject(error_response, "message", "Division by zero");
            cJSON_AddNumberToObject(error_response, "statusCode", 400);
            *response = cJSON_PrintUnformatted(error_response);
            cJSON_Delete(error_response);
            cJSON_Delete(json);
            return;
        }
        result = divide(op1, op2);
    }
    
    // Generate a simple ID (in a real app, use a proper UUID generator)
    char id[37];
    snprintf(id, sizeof(id), "%ld", (long)time(NULL));
    
    // Get current time
    time_t now = time(NULL);
    char time_str[21];
    strftime(time_str, sizeof(time_str), "%Y-%m-%dT%H:%M:%SZ", gmtime(&now));
    
    cJSON *calculation_response = cJSON_CreateObject();
    cJSON_AddStringToObject(calculation_response, "id", id);
    cJSON_AddNumberToObject(calculation_response, "operand1", op1);
    cJSON_AddNumberToObject(calculation_response, "operand2", op2);
    cJSON_AddStringToObject(calculation_response, "operation", op);
    cJSON_AddNumberToObject(calculation_response, "result", result);
    cJSON_AddStringToObject(calculation_response, "createdAt", time_str);
    
    *status_code = 201;
    *response = cJSON_PrintUnformatted(calculation_response);
    
    cJSON_Delete(calculation_response);
    cJSON_Delete(json);
}