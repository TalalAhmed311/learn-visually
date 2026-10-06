#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int x = 100;
    int rc = fork();
    if (rc == 0) {                 // child
        x = x + 1;
        printf("child : x = %d at %p\n", x, (void *) &x);
    } else {                       // parent
        wait(NULL);
        x = x - 1;
        printf("parent: x = %d at %p\n", x, (void *) &x);
    }
    return 0;
}
