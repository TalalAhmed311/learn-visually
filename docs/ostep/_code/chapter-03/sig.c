#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

static volatile sig_atomic_t got = 0;
static void on_term(int sig) { got = sig; }   // handler: just record it

int main(void) {
    pid_t pid = fork();
    if (pid == 0) {                                   // child
        struct sigaction sa = { 0 };
        sa.sa_handler = on_term;
        sigaction(SIGTERM, &sa, NULL);                // catch SIGTERM
        while (!got) pause();                         // sleep until a signal arrives
        printf("child : caught signal %d, cleaning up\n", got);
        exit(0);
    }
    sleep(1);
    kill(pid, SIGTERM);                               // polite request to stop
    int status;
    waitpid(pid, &status, 0);
    printf("parent: child exited normally? %s\n", WIFEXITED(status) ? "yes" : "no");

    pid = fork();
    if (pid == 0) { while (1) pause(); }              // a child that ignores nothing, catches nothing
    kill(pid, SIGKILL);                               // cannot be caught or ignored
    waitpid(pid, &status, 0);
    printf("parent: second child killed by signal %d\n", WTERMSIG(status));
    return 0;
}
