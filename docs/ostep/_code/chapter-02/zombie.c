#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();                 // create a child process (Chapter 03)
    if (pid < 0) { perror("fork"); exit(1); }
    if (pid == 0) {                     // child
        printf("child  %d: exiting with status 3\n", (int) getpid());
        exit(3);                        // child finishes immediately...
    }
    sleep(2);                           // ...but the parent doesn't wait() yet
    printf("parent %d: child %d is now a zombie:\n", (int) getpid(), (int) pid);
    fflush(stdout);
    char cmd[64];
    snprintf(cmd, sizeof cmd, "ps -o pid,stat,cmd -p %d", (int) pid);
    system(cmd);

    int status;
    waitpid(pid, &status, 0);           // reap it: read exit code, free its PCB
    printf("parent: reaped child, exit status = %d\n", WEXITSTATUS(status));
    system(cmd);                        // the child is gone now
    return 0;
}
