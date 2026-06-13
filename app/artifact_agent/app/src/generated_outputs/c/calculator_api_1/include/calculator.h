#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <stdbool.h>

typedef enum {
    OP_ADD,
    OP_SUBTRACT,
    OP_MULTIPLY,
    OP_DIVIDE
} OperationType;

typedef struct {
    double operand1;
    double operand2;
    OperationType operation;
} CalculationRequest;

typedef struct {
    char* id;
    double operand1;
    double operand2;
    OperationType operation;
    double result;
    char* createdAt;
} CalculationResponse;

typedef struct {
    char* error;
    char* message;
    int statusCode;
} ErrorResponse;

bool calculate(const CalculationRequest* request, CalculationResponse* response, ErrorResponse* error);

#endif