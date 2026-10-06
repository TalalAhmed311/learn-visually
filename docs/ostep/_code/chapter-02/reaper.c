#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

static void show_children(void) {
    char cmd[80];
    snprintf(cmd, sizeof cmd, "ps -o pid,ppid,stat,cmd --ppid %d", (int) getpid());
    fflush(stdout);
    system(cmd);
}

int main(void) {
    for (int i = 0; i < 3; i++) {           // a "server" starts 3 workers
        pid_t pid = fork();
        if (pid == 0) exit(i);              // each worker finishes at once
    }
    sleep(1);
    printf("before reaping:\n");
    show_children();                        // 3 zombies (plus ps itself)

    int status; pid_t done;
    while ((done = waitpid(-1, &status, WNOHANG)) > 0)    // reap every finished child
        printf("reaped %d (exit %d)\n", (int) done, WEXITSTATUS(status));

    printf("after reaping:\n");
    show_children();
    return 0;
}
