#ifndef COMMON_H
#define COMMON_H
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <pthread.h>

/* Wall-clock time in seconds, with microsecond resolution. */
static inline double GetTime(void) {
    struct timeval t;
    int rc = gettimeofday(&t, NULL);
    assert(rc == 0);
    return (double) t.tv_sec + (double) t.tv_usec / 1e6;
}

/* Busy-wait (burn CPU) for `howlong` seconds. */
static inline void Spin(int howlong) {
    double t = GetTime();
    while ((GetTime() - t) < (double) howlong)
        ; /* do nothing in loop */
}

/* pthread_create, but abort if it fails. */
static inline void Pthread_create(pthread_t *t, const pthread_attr_t *attr,
                           void *(*start)(void *), void *arg) {
    int rc = pthread_create(t, attr, start, arg);
    assert(rc == 0);
}

static inline void Pthread_join(pthread_t t, void **ret) {
    int rc = pthread_join(t, ret);
    assert(rc == 0);
}
#endif
