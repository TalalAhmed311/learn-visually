#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "common.h"

int main(void) {
    int *p = malloc(sizeof(int));                          // a1
    assert(p != NULL);
    printf("(%d) address pointed to by p: %p\n",
           (int) getpid(), (void *) p);                    // a2
    *p = 0;                                                // a3
    while (1) {
        Spin(1);
        *p = *p + 1;
        printf("(%d) p: %d\n", (int) getpid(), *p);        // a4
        fflush(stdout);
    }
    return 0;
}
