#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <time.h>

#define N 1000000

__attribute__((noinline)) long plain_function(void) {
    return 42;                 // an ordinary procedure call
}

static double now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1e9 + ts.tv_nsec;
}

int main(void) {
    volatile long sink = 0;

    double t0 = now_ns();
    for (int i = 0; i < N; i++)
        sink += plain_function();
    double t1 = now_ns();
    for (int i = 0; i < N; i++)
        sink += syscall(SYS_getpid);   // forces a real trap into the kernel
    double t2 = now_ns();

    printf("procedure call: %6.1f ns each\n", (t1 - t0) / N);
    printf("system call   : %6.1f ns each\n", (t2 - t1) / N);
    return 0;
}
