#include <stdio.h>

/* A toy "process list" and two interchangeable scheduling policies.
   The mechanism (run_all) never changes; only the policy function does. */

struct proc { const char *name; int work; int done; };

typedef int (*policy_fn)(struct proc *p, int n);

/* Policy 1: first in the list that isn't finished (FIFO). */
static int pick_fifo(struct proc *p, int n) {
    for (int i = 0; i < n; i++)
        if (!p[i].done) return i;
    return -1;
}

/* Policy 2: the unfinished process with the least work (shortest first). */
static int pick_shortest(struct proc *p, int n) {
    int best = -1;
    for (int i = 0; i < n; i++)
        if (!p[i].done && (best < 0 || p[i].work < p[best].work)) best = i;
    return best;
}

/* Mechanism: repeatedly ask the policy which process to run, then run it. */
static void run_all(struct proc *p, int n, policy_fn pick, const char *label) {
    printf("%-9s:", label);
    int t = 0, i;
    while ((i = pick(p, n)) >= 0) {
        t += p[i].work;                     // "run" it to completion
        p[i].done = 1;
        printf(" %s(ends at %d)", p[i].name, t);
    }
    printf("\n");
    for (int k = 0; k < n; k++) p[k].done = 0;   // reset for the next run
}

int main(void) {
    struct proc list[] = { {"A", 30, 0}, {"B", 10, 0}, {"C", 20, 0} };
    run_all(list, 3, pick_fifo, "FIFO");
    run_all(list, 3, pick_shortest, "shortest");
    return 0;
}
