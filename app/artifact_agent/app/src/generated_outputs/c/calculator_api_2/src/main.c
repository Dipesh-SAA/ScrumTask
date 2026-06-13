#include <stdio.h>
#include <ulfius.h>
#include <signal.h>
#include "calculations.h"

#define PORT 8080

volatile sig_atomic_t keep_running = 1;

void handle_signal(int sig) {
    keep_running = 0;
}

int main() {
    struct _u_instance instance;
    
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);
    
    if (ulfius_init_instance(&instance, PORT, NULL, NULL) != U_OK) {
        fprintf(stderr, "Error initializing instance\n");
        return 1;
    }
    
    init_calculations();
    
    ulfius_add_endpoint_by_val(&instance, "POST", "/calculations", NULL, 0, &create_calculation, NULL);
    ulfius_add_endpoint_by_val(&instance, "GET", "/calculations/:id", NULL, 0, &get_calculation, NULL);
    ulfius_add_endpoint_by_val(&instance, "PUT", "/calculations/:id", NULL, 0, &update_calculation, NULL);
    ulfius_add_endpoint_by_val(&instance, "DELETE", "/calculations/:id", NULL, 0, &delete_calculation, NULL);
    
    if (ulfius_start_framework(&instance) == U_OK) {
        printf("Calculator API started on port %d\n", instance.port);
        while (keep_running) {
            sleep(1);
        }
    } else {
        fprintf(stderr, "Error starting framework\n");
    }
    
    ulfius_stop_framework(&instance);
    ulfius_clean_instance(&instance);
    
    return 0;
}