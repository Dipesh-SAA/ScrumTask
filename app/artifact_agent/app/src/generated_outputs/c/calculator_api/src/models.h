#ifndef MODELS_H
#define MODELS_H

typedef struct {
    double operand1;
    double operand2;
    const char *operation;
} CalculationCreateRequest;

typedef struct {
    char *id;
    double operand1;
    double operand2;
    const char *operation;
    double result;
    char *createdAt;
} CalculationResponse;

typedef struct {
    const char *error;
    const char *message;
    int statusCode;
} ErrorResponse;

#endif // MODELS_H