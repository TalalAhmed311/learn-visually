# Chapter 01 — tested code

Modernized, self-contained versions of the OSTEP Chapter 2 examples, plus fixes
used on the study page. Built and run on Linux x86-64, gcc 13.3:

    gcc -Wall -Wextra -pthread -o threads threads.c

`common.h` re-creates the helpers (`Spin`, `GetTime`, `Pthread_create`,
`Pthread_join`) that the book's code relies on.
