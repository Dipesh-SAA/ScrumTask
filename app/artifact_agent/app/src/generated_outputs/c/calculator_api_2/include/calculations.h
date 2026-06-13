#ifndef CALCULATIONS_H
#define CALCULATIONS_H

#include <ulfius.h>
#include <jansson.h>

#define MAX_CALCULATIONS 100

typedef struct {
    double operand1;
    double operand2;
    char operation[10];
    double result;
} Calculation;

typedef struct {
    char id[37];
    Calculation calculation;
    char created_at[21];
    char updated_at[21];
} CalculationRecord;

void init_calculations();
int create_calculation(const struct _u_request *request, struct _u_response *response, void *user_data);
int get_calculation(const struct _u_request *request, struct _u_response *response, void *user_data);
int update_calculation(const struct _u_request *request, struct _u_response *response, void *user_data);
int delete_calculation(const struct _u_request *request, struct _u_response *response, void *user_data);

#endif