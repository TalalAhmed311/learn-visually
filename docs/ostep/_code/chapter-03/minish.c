#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(void) {
    char line[256];
    while (printf("minish> "), fflush(stdout), fgets(line, sizeof line, stdin)) {
        char *argv[32], *out = NULL;
        int argc = 0;
        for (char *w = strtok(line, " \t\n"); w && argc < 31; w = strtok(NULL, " \t\n")) {
            if (strcmp(w, ">") == 0) { out = strtok(NULL, " \t\n"); break; }
            argv[argc++] = w;
        }
        argv[argc] = NULL;
        if (argc == 0) continue;
        if (strcmp(argv[0], "exit") == 0) break;      // a built-in: must run in the shell itself

        pid_t pid = fork();
        if (pid < 0) { perror("fork"); continue; }
        if (pid == 0) {                                // child
            if (out) {                                 // redirection, between fork and exec
                int fd = open(out, O_CREAT | O_WRONLY | O_TRUNC, 0644);
                if (fd < 0) { perror(out); exit(1); }
                dup2(fd, STDOUT_FILENO);
                close(fd);
            }
            execvp(argv[0], argv);
            perror(argv[0]);                           // only reached if exec failed
            exit(127);
        }
        int status;
        waitpid(pid, &status, 0);                      // parent: wait for the command
        if (WIFEXITED(status) && WEXITSTATUS(status) != 0)
            printf("[exit %d]\n", WEXITSTATUS(status));
    }
    return 0;
}
