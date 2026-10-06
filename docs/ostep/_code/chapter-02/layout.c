#include <stdio.h>
#include <stdlib.h>

int initialized = 42;          // static data (.data)
int zeroed;                    // static data (.bss)

int main(int argc, char *argv[]) {
    int local = 7;                          // lives on the stack
    int *heap = malloc(sizeof(int));        // lives on the heap

    printf("code   (main)        : %p\n", (void *) main);
    printf("static (initialized) : %p\n", (void *) &initialized);
    printf("static (zeroed)      : %p\n", (void *) &zeroed);
    printf("heap   (malloc)      : %p\n", (void *) heap);
    printf("stack  (local)       : %p\n", (void *) &local);
    printf("argc = %d, argv[0] = %s\n", argc, argv[0]);

    free(heap);
    return 0;
}
