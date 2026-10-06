# Plan — Operating Systems: Three Easy Pieces

- **Source:** `Operating Systems - Three Easy Pieces.pdf`, version 0.90 (© 2014), Remzi H. Arpaci-Dusseau & Andrea C. Arpaci-Dusseau. 675 pages, with PDF bookmarks.
- **Slug:** `ostep`
- **Audience:** developers with 1–2 years of experience who can read C.
- **Code version:** examples are C (C99/C11) on Linux, compiled with gcc 13. Book code relies on a `common.h` helper header that the PDF does not print; we re-create it. Any rewritten/modernized code is marked as such on the page. Tested sources live in `_code/chapter-NN/`.

## Core goal

Explain how an operating system works by building it up from three ideas: **virtualization** (turning one CPU and one memory into many private ones), **concurrency** (running many things at once correctly), and **persistence** (keeping data safe on devices that fail). Each chapter states a "crux" problem and works towards the mechanisms (how) and policies (which) that solve it.

**Prerequisites assumed:** what a program is, basic C (pointers, `malloc`, structs), a rough idea of CPU/RAM/disk, using a Unix shell.

## Chapter mapping

Book dialogues (2-page conversations) are folded into the next teaching chapter; parts become groups on the book index.

| Study | Book | Title | Purpose | Core concepts | Key code | Prereqs |
|---|---|---|---|---|---|---|
| **Intro** |||||||
| 01 | 1–2 | Introduction to Operating Systems | Big-picture tour: what an OS is and the three pieces | von Neumann cycle; OS as virtual machine / standard library / resource manager; CPU virtualization; memory virtualization; concurrency; persistence; user vs kernel mode & system calls; design goals; history | `cpu.c`, `mem.c`, `threads.c`, `io.c` | — |
| **Part I — Virtualization** |||||||
| 02 | 3–4 | The Abstraction: The Process | What a process is | process = running program; machine state (memory, registers, PC, SP); process API; creation (load, stack, heap, fds); states (running/ready/blocked); PCB / process list | process list struct (xv6 `proc`) | 01 |
| 03 | 5 | Interlude: Process API | Creating/controlling processes | `fork()`, `wait()`, `exec()`; why split fork/exec (shell redirection); signals, `kill` | `p1.c`–`p4.c` | 02 |
| 04 | 6 | Limited Direct Execution | Run programs fast but safely | direct execution; user/kernel mode; trap & trap table; timer interrupt; context switch; cooperative vs preemptive | `swtch` pseudo-asm | 02, 03 |
| 05 | 7 | Scheduling: Introduction | Basic scheduling policies | workload assumptions; turnaround & response time; FIFO; SJF; STCF; Round Robin; overlapping I/O | — (simulator) | 04 |
| 06 | 8 | Scheduling: MLFQ | Learn job behaviour without an oracle | MLFQ rules 1–5; priority boost; gaming & accounting; tuning (Solaris tables) | — | 05 |
| 07 | 9 | Scheduling: Proportional Share | Fairness via tickets | lottery scheduling; ticket currency/transfer/inflation; stride scheduling; unfairness metric | lottery decision code | 05 |
| 08 | 10–11 | Multiprocessor Scheduling | Scheduling on many CPUs | caches & coherence; synchronization; cache affinity; SQMS vs MQMS; load imbalance & work stealing; O(1)/CFS/BFS | — | 05, 07 |
| 09 | 12–13 | Address Spaces | Memory virtualization goal | early systems; multiprogramming & time sharing; address space layout (code/heap/stack); transparency, efficiency, protection | print addresses | 01, 02 |
| 10 | 14 | Interlude: Memory API | Using `malloc`/`free` correctly | stack vs heap; `malloc`/`free`/`calloc`/`realloc`; common errors (leaks, dangling, double free, uninit reads); `brk`/`mmap` | buggy vs fixed snippets | 09 |
| 11 | 15 | Address Translation | Base & bounds | dynamic relocation; MMU; base/bounds registers; OS duties (free list, save/restore, exceptions) | translation pseudo-code | 09, 04 |
| 12 | 16 | Segmentation | Generalized base/bounds | segments; segment selection by address bits; negative-growing stack; protection bits & sharing; external fragmentation | address-split code | 11 |
| 13 | 17 | Free-Space Management | Allocators | splitting & coalescing; header/magic; embedded free list; best/worst/first/next fit; segregated lists; slab; buddy | free-list structs | 10, 12 |
| 14 | 18 | Paging: Introduction | Fixed-size pages | VPN/offset; page tables & PTE bits; where tables live; memory trace & cost | translation code | 12 |
| 15 | 19 | TLBs | Caching translations | TLB algorithm; locality; HW vs SW miss handling; ASIDs & context switches; replacement; MIPS TLB entry | TLB control-flow code | 14 |
| 16 | 20 | Paging: Smaller Tables | Shrinking page tables | bigger pages; paging+segments hybrid; multi-level tables; inverted tables; swapping tables | multi-level lookup code | 14, 15 |
| 17 | 21 | Swapping: Mechanisms | Beyond physical memory | swap space; present bit; page fault & handler; high/low watermarks, swap daemon | page-fault control flow | 16 |
| 18 | 22 | Swapping: Policies | Which page to evict | AMAT; optimal; FIFO (Belady's anomaly); random; LRU; workloads; clock; dirty pages; thrashing | — (simulator) | 17 |
| 19 | 23–24 | The VAX/VMS VM System | A real VM system | segmented FIFO; page clustering; demand zeroing; copy-on-write; layout (kernel in every address space) | — | 14–18 |
| **Part II — Concurrency** |||||||
| 20 | 25–26 | Concurrency: An Introduction | Threads and races | thread vs process; shared data; race conditions; critical sections; atomicity; mutual exclusion; waiting | `t0.c`, `t1.c` | 01, 04 |
| 21 | 27 | Interlude: Thread API | Using pthreads | `pthread_create/join`; mutexes; condition variables; compile flags | API snippets | 20 |
| 22 | 28 | Locks | Building locks | goals (correctness, fairness, performance); disabling interrupts; test-and-set, CAS, LL/SC, fetch-and-add (ticket lock); spinning vs yielding vs queues (futex); two-phase locks | spin lock, ticket lock | 21 |
| 23 | 29 | Lock-based Data Structures | Concurrent counters/lists/queues/hash | approximate (sloppy) counter; hand-over-hand locking; two-lock queue; per-bucket hash locks | counter, queue | 22 |
| 24 | 30 | Condition Variables | Waiting for conditions | wait/signal; join; producer/consumer; Mesa semantics → `while`; two CVs; covering conditions | bounded buffer | 22 |
| 25 | 31 | Semaphores | One primitive for both | sem_wait/post; binary semaphores; ordering; bounded buffer; reader-writer locks; dining philosophers; implementing semaphores | semaphore solutions | 24 |
| 26 | 32 | Common Concurrency Problems | Bug taxonomy | atomicity & order violations; deadlock conditions; prevention (ordering, trylock, lock-free); avoidance (Banker-like scheduling); detect & recover | deadlocking code | 22–25 |
| 27 | 33–34 | Event-based Concurrency | Event loops | event loop; `select`/`poll`; no locks needed; blocking calls problem; async I/O; manual stack management/continuations | `select()` server | 20 |
| **Part III — Persistence** |||||||
| 28 | 35–36 | I/O Devices | How the OS talks to devices | system bus hierarchy; canonical device; polling; interrupts; DMA; port vs memory-mapped I/O; device drivers; IDE driver | xv6 IDE driver | 04 |
| 29 | 37 | Hard Disk Drives | Disk mechanics & math | geometry; seek/rotation/transfer; I/O time & rate math; track skew, caches; SSTF, elevator (SCAN/C-SCAN), SPTF | — (calculator) | 28 |
| 30 | 38 | RAID | Arrays of disks | fault model; capacity/reliability/performance; RAID 0, 1, 4, 5; small-write problem; comparison | — (simulator) | 29 |
| 31 | 39 | Files and Directories | The file-system API | files & inodes numbers; open/read/write/lseek; fsync; rename atomicity; stat; unlink; directories; hard & symbolic links; mkfs & mount | API snippets | 01 |
| 32 | 40 | File System Implementation | vsfs, a simple FS | on-disk layout (superblock, bitmaps, inodes, data); inode & multi-level index; directories; free space; read/write access paths; caching & buffering | — (layout explorer) | 31 |
| 33 | 41 | Locality & FFS | Disk-aware FS | poor locality in old FS; cylinder groups; placement policies; large-file exception; sub-blocks, parameterization | — | 29, 32 |
| 34 | 42 | Crash Consistency | Surviving crashes | crash scenarios; fsck; data & metadata journaling; checkpoint; revoke; ordered journaling; soft updates, COW, backpointers | — (crash simulator) | 32 |
| 35 | 43 | Log-structured FS | Write everything sequentially | segments; buffering amount; inode map; checkpoint region; directories; garbage collection; liveness; crash recovery | — | 32, 34 |
| 36 | 44–45 | Data Integrity | Detecting corruption | LSEs & corruption; RAID recovery; checksums (XOR, Fletcher, CRC); misdirected & lost writes; scrubbing; overheads | checksum code | 30, 32 |
| 37 | 46–47 | Distributed Systems | Communication basics | packet loss; UDP; reliable messaging (acks, timeouts, retries, sequence numbers); DSM vs RPC; stubs, marshaling | UDP client/server | 01 |
| 38 | 48 | NFS | Stateless distributed FS | client/server FS; statelessness & file handles; NFSv2 protocol; idempotency; client caching & consistency; flush-on-close | — | 31, 37 |
| 39 | 49–50 | AFS | Scalable distributed FS | whole-file caching; callbacks; consistency semantics; crash recovery; scale | — | 38 |
| **Appendices** |||||||
| 40 | A–B | Virtual Machine Monitors | Virtualizing the OS itself | VMM; limited direct execution for OSes; trap handling; virtualizing memory (shadow tables); information gap | — | 04, 15 |
| 41 | I | Flash-based SSDs | How SSDs work | cells/pages/blocks; erase-before-write; FTL; log-structured FTL; garbage collection; mapping table size; wear leveling | — | 35 |
| 42 | E–F | Lab Tutorial | The C toolchain | compiling & linking; flags; `make`; `gdb`; man pages | Makefile, gdb session | — |

## Concept dependency graph

```
Ch01 Intro
 ├─► Process (02) ─► Process API (03)
 │      └─► LDE (04) ─► Scheduling (05) ─► MLFQ (06)
 │                         ├─► Lottery/Stride (07) ─► Multiprocessor (08)
 │                         └─► VMM (40)
 ├─► Address spaces (09) ─► Memory API (10) ─► Free-space (13)
 │      └─► Base/bounds (11) ─► Segmentation (12) ─► Paging (14) ─► TLB (15) ─► Smaller tables (16)
 │                                                     └─► Swap mech (17) ─► Swap policy (18) ─► VAX/VMS (19)
 ├─► Concurrency intro (20) ─► Thread API (21) ─► Locks (22) ─► Lock-based DS (23)
 │                                  └─► CVs (24) ─► Semaphores (25) ─► Concurrency bugs (26)
 │      └─► Event-based (27)
 └─► I/O devices (28) ─► HDD (29) ─► RAID (30) ─► Data integrity (36)
        Files & dirs (31) ─► FS impl (32) ─► FFS (33) / Crash consistency (34) ─► LFS (35) ─► SSDs (41)
        Distributed (37) ─► NFS (38) ─► AFS (39)
```

## Recurring terms (define the same way everywhere)

| Term | Definition used across all chapters |
|---|---|
| Operating system (OS) | Software that makes the machine easy to use and safe to share: it virtualizes resources, provides system calls, and manages resources. |
| Kernel | The part of the OS that runs in kernel mode with full hardware access. |
| Virtualization | Turning a physical resource into a more general, easier-to-use virtual form; often giving each program the illusion of its own copy. |
| Process | A running program: its address space, registers, and OS bookkeeping. |
| Thread | One stream of execution; threads in the same process share an address space. |
| Address space | The private range of (virtual) addresses a process sees. |
| Mechanism | Low-level method or protocol that implements a piece of functionality (the *how*). |
| Policy | Algorithm that makes a decision using mechanisms (the *which*). |
| System call | Controlled entry into the kernel via a trap instruction, raising privilege. |
| Trap | Hardware instruction/event that jumps into the kernel and raises privilege to kernel mode. |
| User mode / kernel mode | Restricted vs privileged CPU execution modes. |
| Context switch | Saving one process's registers and restoring another's. |
| Race condition | Outcome depends on the timing of interleaved execution. |
| Critical section | Code that accesses a shared resource and must not be run by two threads at once. |
| Atomic | Happens all at once or not at all, from everyone else's point of view. |
| Persistence | Data survives power loss or crashes. |
| File system | OS software that stores files on devices reliably and efficiently. |
| Device driver | OS code that knows how to operate one specific device. |

## Theme / design system — "phosphor terminal"

- **Motif:** a terminal/CRT look: `$` prompts, block cursors, box-drawing borders, subtle scanlines in the hero, layered "stack" diagrams (apps / OS / hardware).
- **Theme (current):** "Calm" — graphite dark default + light mode, one muted teal accent, muted semantic diagram colors, no decorative animation. Fonts: Inter + JetBrains Mono. (Replaced the original "phosphor terminal" design after review.)
- **Fonts (original design):** headings *Space Grotesk*, body *IBM Plex Sans*, code & labels *JetBrains Mono*.
- **Colors (CSS variables, dark is default look, light is "paper terminal"):**
  - `--accent` phosphor green — user programs / processes / "the good path"
  - `--kernel` amber — the OS / kernel mode
  - `--hw` cyan — hardware (CPU, RAM, disk, MMU)
  - `--danger` red — bugs, races, crashes
  - `--violet` — persistence / storage data
- These **semantic colors are fixed for every chapter**, so a reader learns "amber = kernel" once.
- Shared layout across all books: `src/shared/base.css` + `src/shared/base.js`; book theme in `src/ostep/theme.css`. `tools/build.py` inlines them into each self-contained page.

## Per-chapter visual choices

### Chapter 01 — Introduction to Operating Systems
| Concept | Visual | Interaction |
|---|---|---|
| Running a program (von Neumann) | CPU + memory diagram | fetch–decode–execute stepper (play/pause/step) on a toy ISA |
| What an OS is | Layered architecture diagram (apps → syscalls → kernel subsystems → HW) | — |
| Virtualizing the CPU | Gantt timeline of A/B/C/D on one CPU | Lab 1: time-sharing simulator (time-slice + switch-cost sliders) |
| Virtualizing memory | Two address spaces mapped to physical memory | Click-to-increment memory mapper |
| Concurrency | Interleaving sequence diagram | Lab 2: race-condition stepper + "run N times" experiment |
| Persistence | Sequence diagram: process → kernel → FS → cache → driver → disk | — |
| User vs kernel mode | State machine (user ⇄ kernel via trap / return-from-trap) + table: procedure call vs system call | Drag-to-order the system call steps |
| Design goals | Comparison table (goal / meaning / cost / where in book) | — |
| History | Timeline SVG | — |
| Multiprogramming payoff | Chart.js utilization curve | Lab 3: slider for I/O wait fraction (simplified model, flagged) |

### Chapter 02 — The Abstraction: The Process
| Concept | Visual | Interaction |
|---|---|---|
| Time vs space sharing | Side-by-side CPU timeline vs disk block grid + comparison table | — |
| Mechanism vs policy | Layer diagram (policy over mechanism) | — (runnable `policy.c`) |
| Machine state | Memory-layout diagram with registers and fd table | — (runnable `layout.c`) |
| Process API | Operation → UNIX table; real `ps`/`kill` transcript | — |
| Process creation | Disk → memory loading diagram | Step-through loader (play/pause/step) |
| Process states | State machine + book trace tables + Linux STAT mapping | Event buttons driving the state machine |
| Process list / PCB | xv6 `struct proc` annotated | Context-switch save/restore widget; `zombie.c` |
| Lab | Process-state simulator (process-run.py-like) | Presets incl. book Figs 4.3/4.4, policies for I/O |

## Uncertainties / notes
- Ch02: The PDF pages for book chapter 4 say version 0.91 (chapters 1–2 say 0.90).
- Ch02: The lab simulator is our own, inspired by `process-run.py`; its timing rules are stated on the page and reproduce the book's Figures 4.3 and 4.4 exactly, but may differ in detail from the real script.
- Ch01: The book's `io.c` writes 13 bytes for `"hello world\n"` (12 visible chars), so the file gets a trailing NUL byte — verified with `od -c`. The page points this out and uses `strlen`.
- Ch01: The book's `mem.c` prints a pointer with `%08x` and an `(unsigned)` cast, which truncates 64-bit pointers; the page modernizes to `%p`.
- Ch01: Book's shell line `./cpu A & ; ./cpu B & ...` is tcsh syntax; bash equivalent given.
