#ifndef ROUTES_H
#define ROUTES_H

void setup_routes();
void handle_create_calculation(const char *request_body, char **response, int *status_code);

#endif // ROUTES_H