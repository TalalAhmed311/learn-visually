#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    printf("hello world (pid:%d)\n", (int) getpid());
    fflush(stdout);
    int rc = fork();
    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {         // child: become "wc p3.c"
        printf("hello, I am child (pid:%d)\n", (int) getpid());
        fflush(stdout);
        char *myargs[] = { "wc", "p3.c", NULL };   // argv for the new program
        execvp(myargs[0], myargs);                 // only returns on error
        perror("execvp");
        exit(1);
    } else {                      // parent
        int wc = wait(NULL);
        printf("hello, I am parent of %d (wc:%d) (pid:%d)\n", rc, wc, (int) getpid());
    }
    return 0;
}
