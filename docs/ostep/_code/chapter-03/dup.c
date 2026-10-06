#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("before fork ");        // no newline: stays in the stdio buffer
    if (fork() == 0) {
        printf("child\n");
    } else {
        wait(NULL);
        printf("parent\n");
    }
    return 0;
}
