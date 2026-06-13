#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <ulfius.h>
#include <jansson.h>
#include "calculations.h"
#include "utils.h"

static CalculationRecord calculations[MAX_CALCULATIONS];
static int calculation_count = 0;

void init_calculations() {
    calculation_count = 0;
    memset(calculations, 0, sizeof(calculations));
}

int create_calculation(const struct _u_request *request, struct _u_response *response, void *user_data) {
    json_error_t error;
    json_t *json_body = ulfius_get_json_body_request(request, &error);
    
    if (!json_body) {
        send_error_response(response, 400, "Bad Request", "Invalid JSON body");
        return U_CALLBACK_ERROR;
    }
    
    json_t *validated = validate_calculation_request(json_body, 1);
    if (!validated) {
        send_error_response(response, 400, "Bad Request", "Invalid calculation request");
        json_decref(json_body);
        return U_CALLBACK_ERROR;
    }
    
    double operand1 = json_number_value(json_object_get(validated, "operand1"));
    double operand2 = json_number_value(json_object_get(validated, "operand2"));
    const char *operation = json_string_value(json_object_get(validated, "operation"));
    
    double result = perform_operation(operand1, operand2, operation);
    if (isnan(result)) {
        send_error_response(response, 400, "Bad Request", "Invalid operation or division by zero");
        json_decref(json_body);
        json_decref(validated);
        return U_CALLBACK_ERROR;
    }
    
    if (calculation_count >= MAX_CALCULATIONS) {
        send_error_response(response, 500, "Internal Server Error", "Maximum calculations reached");
        json_decref(json_body);
        json_decref(validated);
        return U_CALLBACK_ERROR;
    }
    
    CalculationRecord *record = &calculations[calculation_count++];
    strncpy(record->id, generate_uuid(), sizeof(record->id) - 1);
    record->calculation.operand1 = operand1;
    record->calculation.operand2 = operand2;
    strncpy(record->calculation.operation, operation, sizeof(record->calculation.operation) - 1);
    record->calculation.result = result;
    strncpy(record->created_at, get_current_timestamp(), sizeof(record->created_at) - 1);
    strncpy(record->updated_at, record->created_at, sizeof(record->updated_at) - 1);
    
    json_t *response_json = json_object();
    json_object_set_new(response_json, "id", json_string(record->id));
    json_object_set_new(response_json, "operand1", json_real(record->calculation.operand1));
    json_object_set_new(response_json, "operand2", json_real(record->calculation.operand2));
    json_object_set_new(response_json, "operation", json_string(record->calculation.operation));
    json_object_set_new(response_json, "result", json_real(record->calculation.result));
    json_object_set_new(response_json, "createdAt", json_string(record->created_at));
    json_object_set_new(response_json, "updatedAt", json_string(record->updated_at));
    
    ulfius_set_json_body_response(response, 201, response_json);
    json_decref(response_json);
    json_decref(json_body);
    json_decref(validated);
    
    return U_CALLBACK_CONTINUE;
}

int get_calculation(const struct _u_request *request, struct _u_response *response, void *user_data) {
    const char *id = u_map_get(request->map_url, "id");
    
    if (!id) {
        send_error_response(response, 400, "Bad Request", "Missing calculation ID");
        return U_CALLBACK_ERROR;
    }
    
    for (int i = 0; i < calculation_count; i++) {
        if (strcmp(calculations[i].id, id) == 0) {
            json_t *response_json = json_object();
            json_object_set_new(response_json, "id", json_string(calculations[i].id));
            json_object_set_new(response_json, "operand1", json_real(calculations[i].calculation.operand1));
            json_object_set_new(response_json, "operand2", json_real(calculations[i].calculation.operand2));
            json_object_set_new(response_json, "operation", json_string(calculations[i].calculation.operation));
            json_object_set_new(response_json, "result", json_real(calculations[i].calculation.result));
            json_object_set_new(response_json, "createdAt", json_string(calculations[i].created_at));
            json_object_set_new(response_json, "updatedAt", json_string(calculations[i].updated_at));
            
            ulfius_set_json_body_response(response, 200, response_json);
            json_decref(response_json);
            return U_CALLBACK_CONTINUE;
        }
    }
    
    send_error_response(response, 404, "Not Found", "Calculation not found");
    return U_CALLBACK_ERROR;
}

int update_calculation(const struct _u_request *request, struct _u_response *response, void *user_data) {
    const char *id = u_map_get(request->map_url, "id");
    
    if (!id) {
        send_error_response(response, 400, "Bad Request", "Missing calculation ID");
        return U_CALLBACK_ERROR;
    }
    
    json_error_t error;
    json_t *json_body = ulfius_get_json_body_request(request, &error);
    
    if (!json_body) {
        send_error_response(response, 400, "Bad Request", "Invalid JSON body");
        return U_CALLBACK_ERROR;
    }
    
    json_t *validated = validate_calculation_request(json_body, 0);
    if (!validated) {
        send_error_response(response, 400, "Bad Request", "Invalid calculation request");
        json_decref(json_body);
        return U_CALLBACK_ERROR;
    }
    
    for (int i = 0; i < calculation_count; i++) {
        if (strcmp(calculations[i].id, id) == 0) {
            double operand1 = calculations[i].calculation.operand1;
            double operand2 = calculations[i].calculation.operand2;
            const char *operation = calculations[i].calculation.operation;
            
            if (json_object_get(validated, "operand1")) {
                operand1 = json_number_value(json_object_get(validated, "operand1"));
            }
            if (json_object_get(validated, "operand2")) {
                operand2 = json_number_value(json_object_get(validated, "operand2"));
            }
            if (json_object_get(validated, "operation")) {
                operation = json_string_value(json_object_get(validated, "operation"));
            }
            
            double result = perform_operation(operand1, operand2, operation);
            if (isnan(result)) {
                send_error_response(response, 400, "Bad Request", "Invalid operation or division by zero");
                json_decref(json_body);
                json_decref(validated);
                return U_CALLBACK_ERROR;
            }
            
            calculations[i].calculation.operand1 = operand1;
            calculations[i].calculation.operand2 = operand2;
            strncpy(calculations[i].calculation.operation, operation, sizeof(calculations[i].calculation.operation) - 1);
            calculations[i].calculation.result = result;
            strncpy(calculations[i].updated_at, get_current_timestamp(), sizeof(calculations[i].updated_at) - 1);
            
            json_t *response_json = json_object();
            json_object_set_new(response_json, "id", json_string(calculations[i].id));
            json_object_set_new(response_json, "operand1", json_real(calculations[i].calculation.operand1));
            json_object_set_new(response_json, "operand2", json_real(calculations[i].calculation.operand2));
            json_object_set_new(response_json, "operation", json_string(calculations[i].calculation.operation));
            json_object_set_new(response_json, "result", json_real(calculations[i].calculation.result));
            json_object_set_new(response_json, "createdAt", json_string(calculations[i].created_at));
            json_object_set_new(response_json, "updatedAt", json_string(calculations[i].updated_at));
            
            ulfius_set_json_body_response(response, 200, response_json);
            json_decref(response_json);
            json_decref(json_body);
            json_decref(validated);
            return U_CALLBACK_CONTINUE;
        }
    }
    
    send_error_response(response, 404, "Not Found", "Calculation not found");
    json_decref(json_body);
    json_decref(validated);
    return U_CALLBACK_ERROR;
}

int delete_calculation(const struct _u_request *request, struct _u_response *response, void *user_data) {
    const char *id = u_map_get(request->map_url, "id");
    
    if (!id) {
        send_error_response(response, 400, "Bad Request", "Missing calculation ID");
        return U_CALLBACK_ERROR;
    }
    
    for (int i = 0; i < calculation_count; i++) {
        if (strcmp(calculations[i].id, id) == 0) {
            for (int j = i; j < calculation_count - 1; j++) {
                calculations[j] = calculations[j + 1];
            }
            calculation_count--;
            
            ulfius_set_empty_body_response(response, 204);
            return U_CALLBACK_CONTINUE;
        }
    }
    
    send_error_response(response, 404, "Not Found", "Calculation not found");
    return U_CALLBACK_ERROR;
}