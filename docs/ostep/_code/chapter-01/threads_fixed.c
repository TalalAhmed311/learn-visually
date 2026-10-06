#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include "common.h"

atomic_int counter = 0;      // C11 atomic integer
int loops;

void *worker(void *arg) {
    (void) arg;
    for (int i = 0; i < loops; i++) {
        atomic_fetch_add(&counter, 1);   // one indivisible read-modify-write
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: threads_fixed <loops>\n");
        exit(1);
    }
    loops = atoi(argv[1]);
    pthread_t p1, p2;
    printf("Initial value : %d\n", atomic_load(&counter));
    Pthread_create(&p1, NULL, worker, NULL);
    Pthread_create(&p2, NULL, worker, NULL);
    Pthread_join(p1, NULL);
    Pthread_join(p2, NULL);
    printf("Final value   : %d\n", atomic_load(&counter));
    return 0;
}
