#include <stdio.h>
#include <stdlib.h>
#include "common.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "usage: cpu <string>\n");
        exit(1);
    }
    char *str = argv[1];
    while (1) {
        Spin(1);              // burn ~1 second of CPU
        printf("%s\n", str);  // then print our label
        fflush(stdout);
    }
    return 0;
}
