#include "handlers.h"
#include "calculator.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <cjson/cJSON.h>

void handle_create_calculation(const char* request_body, char** response, int* status_code) {
    cJSON* json = cJSON_Parse(request_body);
    if (!json) {
        *status_code = 400;
        cJSON* error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "invalid_json");
        cJSON_AddStringToObject(error_response, "message", "Invalid JSON format");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        return;
    }
    
    cJSON* operand1 = cJSON_GetObjectItemCaseSensitive(json, "operand1");
    cJSON* operand2 = cJSON_GetObjectItemCaseSensitive(json, "operand2");
    cJSON* operation = cJSON_GetObjectItemCaseSensitive(json, "operation");
    
    if (!cJSON_IsNumber(operand1) || !cJSON_IsNumber(operand2) || !cJSON_IsString(operation)) {
        *status_code = 400;
        cJSON* error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "invalid_request");
        cJSON_AddStringToObject(error_response, "message", "Missing or invalid required fields");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        cJSON_Delete(json);
        return;
    }
    
    CalculationRequest request;
    request.operand1 = operand1->valuedouble;
    request.operand2 = operand2->valuedouble;
    
    if (strcmp(operation->valuestring, "add") == 0) {
        request.operation = OP_ADD;
    } else if (strcmp(operation->valuestring, "subtract") == 0) {
        request.operation = OP_SUBTRACT;
    } else if (strcmp(operation->valuestring, "multiply") == 0) {
        request.operation = OP_MULTIPLY;
    } else if (strcmp(operation->valuestring, "divide") == 0) {
        request.operation = OP_DIVIDE;
    } else {
        *status_code = 400;
        cJSON* error_response = cJSON_CreateObject();
        cJSON_AddStringToObject(error_response, "error", "invalid_operation");
        cJSON_AddStringToObject(error_response, "message", "Invalid operation type");
        cJSON_AddNumberToObject(error_response, "statusCode", 400);
        *response = cJSON_PrintUnformatted(error_response);
        cJSON_Delete(error_response);
        cJSON_Delete(json);
        return;
    }
    
    CalculationResponse calc_response;
    ErrorResponse error_response;
    
    if (calculate(&request, &calc_response, &error_response)) {
        *status_code = 201;
        cJSON* response_json = cJSON_CreateObject();
        cJSON_AddStringToObject(response_json, "id", calc_response.id);
        cJSON_AddNumberToObject(response_json, "operand1", calc_response.operand1);
        cJSON_AddNumberToObject(response_json, "operand2", calc_response.operand2);
        
        switch (calc_response.operation) {
            case OP_ADD: cJSON_AddStringToObject(response_json, "operation", "add"); break;
            case OP_SUBTRACT: cJSON_AddStringToObject(response_json, "operation", "subtract"); break;
            case OP_MULTIPLY: cJSON_AddStringToObject(response_json, "operation", "multiply"); break;
            case OP_DIVIDE: cJSON_AddStringToObject(response_json, "operation", "divide"); break;
        }
        
        cJSON_AddNumberToObject(response_json, "result", calc_response.result);
        cJSON_AddStringToObject(response_json, "createdAt", calc_response.createdAt);
        
        *response = cJSON_PrintUnformatted(response_json);
        cJSON_Delete(response_json);
        
        free(calc_response.id);
        free(calc_response.createdAt);
    } else {
        *status_code = error_response.statusCode;
        cJSON* error_json = cJSON_CreateObject();
        cJSON_AddStringToObject(error_json, "error", error_response.error);
        cJSON_AddStringToObject(error_json, "message", error_response.message);
        cJSON_AddNumberToObject(error_json, "statusCode", error_response.statusCode);
        *response = cJSON_PrintUnformatted(error_json);
        cJSON_Delete(error_json);
        
        free(error_response.error);
        free(error_response.message);
    }
    
    cJSON_Delete(json);
}