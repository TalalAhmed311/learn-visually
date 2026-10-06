#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

/* Runs the equivalent of:  grep -o fork p1.c | wc -l  */
int main(void) {
    int fds[2];
    if (pipe(fds) < 0) { perror("pipe"); exit(1); }   // fds[0] = read end, fds[1] = write end

    if (fork() == 0) {                    // first child: grep, writes into the pipe
        dup2(fds[1], STDOUT_FILENO);      // stdout -> pipe's write end
        close(fds[0]); close(fds[1]);
        execlp("grep", "grep", "-o", "fork", "p1.c", (char *) NULL);
        perror("exec grep"); exit(1);
    }
    if (fork() == 0) {                    // second child: wc, reads from the pipe
        dup2(fds[0], STDIN_FILENO);       // stdin -> pipe's read end
        close(fds[0]); close(fds[1]);
        execlp("wc", "wc", "-l", (char *) NULL);
        perror("exec wc"); exit(1);
    }
    close(fds[0]); close(fds[1]);         // parent must close both ends, or wc never sees EOF
    wait(NULL); wait(NULL);
    return 0;
}
