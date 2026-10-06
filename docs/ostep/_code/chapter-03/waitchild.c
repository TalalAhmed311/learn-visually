#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int rc = fork();
    if (rc == 0) {                       // the child has no children of its own
        int r = wait(NULL);
        printf("child : wait() = %d (%s)\n", r, strerror(errno));
        return 7;
    }
    int status;
    int r = wait(&status);
    printf("parent: wait() = %d, child %d exited with %d\n", r, rc, WEXITSTATUS(status));
    return 0;
}
