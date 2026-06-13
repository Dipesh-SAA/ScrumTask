#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "routes.h"
#include "models.h"

#define PORT 8080

int main() {
    printf("Calculator API running on port %d\n", PORT);
    
    // Initialize routes
    setup_routes();
    
    return 0;
}