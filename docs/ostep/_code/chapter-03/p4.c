#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(void) {
    int rc = fork();
    if (rc < 0) {
        fprintf(stderr, "fork failed\n");
        exit(1);
    } else if (rc == 0) {         // child: redirect standard output to a file
        close(STDOUT_FILENO);     // fd 1 is now free
        int fd = open("./p4.output", O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
        if (fd != STDOUT_FILENO) { perror("open"); exit(1); }   // lowest free fd = 1
        char *myargs[] = { "wc", "p4.c", NULL };
        execvp(myargs[0], myargs);   // wc writes to fd 1 = the file
        perror("execvp");
        exit(1);
    } else {
        wait(NULL);
    }
    return 0;
}
