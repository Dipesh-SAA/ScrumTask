#ifndef UTILS_H
#define UTILS_H

#include <ulfius.h>
#include <jansson.h>

json_t* validate_calculation_request(json_t *json_body, int require_operation);
void send_error_response(struct _u_response *response, int status, const char *error, const char *message);
double perform_operation(double operand1, double operand2, const char *operation);
char* generate_uuid();
char* get_current_timestamp();

#endif