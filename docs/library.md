# Library progress log

Books folder: repository root (`/`). Output folder: `docs/` (servable as-is, e.g. via GitHub Pages).

Processing order: the OS book first (as requested), then the rest. Work is paused after
OSTEP chapter 01 for review before continuing.

| # | File | Title | Author | Topic | Format | Chapters | Status |
|---|------|-------|--------|-------|--------|----------|--------|
| 1 | `Operating Systems - Three Easy Pieces.pdf` | Operating Systems: Three Easy Pieces (v0.90) | Remzi H. Arpaci-Dusseau, Andrea C. Arpaci-Dusseau | Operating systems | Text PDF (675 pp., bookmarked) | 42 study chapters (from 50 book chapters + 2 appendices) | **in progress** — 1/42 done |
| 2 | `Inside Machine.pdf` | Inside the Machine: An Illustrated Introduction to Microprocessors and Computer Architecture (2007) | Jon Stokes | Computer architecture | Text PDF (320 pp., bookmarked) | 12 | pending |
| 3 | `Inference Engineering.pdf` | Inference Engineering | Philip Kiely | ML inference / LLM serving | Text PDF (275 pp., bookmarked) | 8 (Ch. 0–7) + glossary appendix | pending |

No duplicates found (one file per title). All three PDFs have a text layer, so no OCR is needed.

## OSTEP chapter status

| Study ch. | Book ch. | Title | Status |
|-----------|----------|-------|--------|
| 01 | 1–2 | Introduction to Operating Systems | done (awaiting review) |
| 02 | 3–4 | The Abstraction: The Process | pending |
| 03 | 5 | Interlude: Process API | pending |
| 04 | 6 | Mechanism: Limited Direct Execution | pending |
| 05 | 7 | Scheduling: Introduction | pending |
| 06 | 8 | Scheduling: The Multi-Level Feedback Queue | pending |
| 07 | 9 | Scheduling: Proportional Share | pending |
| 08 | 10–11 | Multiprocessor Scheduling (Advanced) | pending |
| 09 | 12–13 | The Abstraction: Address Spaces | pending |
| 10 | 14 | Interlude: Memory API | pending |
| 11 | 15 | Mechanism: Address Translation | pending |
| 12 | 16 | Segmentation | pending |
| 13 | 17 | Free-Space Management | pending |
| 14 | 18 | Paging: Introduction | pending |
| 15 | 19 | Paging: Faster Translations (TLBs) | pending |
| 16 | 20 | Paging: Smaller Tables | pending |
| 17 | 21 | Beyond Physical Memory: Mechanisms | pending |
| 18 | 22 | Beyond Physical Memory: Policies | pending |
| 19 | 23–24 | The VAX/VMS Virtual Memory System | pending |
| 20 | 25–26 | Concurrency: An Introduction | pending |
| 21 | 27 | Interlude: Thread API | pending |
| 22 | 28 | Locks | pending |
| 23 | 29 | Lock-based Concurrent Data Structures | pending |
| 24 | 30 | Condition Variables | pending |
| 25 | 31 | Semaphores | pending |
| 26 | 32 | Common Concurrency Problems | pending |
| 27 | 33–34 | Event-based Concurrency (Advanced) | pending |
| 28 | 35–36 | I/O Devices | pending |
| 29 | 37 | Hard Disk Drives | pending |
| 30 | 38 | Redundant Arrays of Inexpensive Disks (RAID) | pending |
| 31 | 39 | Interlude: Files and Directories | pending |
| 32 | 40 | File System Implementation | pending |
| 33 | 41 | Locality and the Fast File System | pending |
| 34 | 42 | Crash Consistency: FSCK and Journaling | pending |
| 35 | 43 | Log-structured File Systems | pending |
| 36 | 44–45 | Data Integrity and Protection | pending |
| 37 | 46–47 | Distributed Systems | pending |
| 38 | 48 | Sun's Network File System (NFS) | pending |
| 39 | 49–50 | The Andrew File System (AFS) | pending |
| 40 | App. A–B | Virtual Machine Monitors | pending |
| 41 | App. I | Flash-based SSDs | pending |
| 42 | App. E–F | Lab Tutorial: The C Development Environment | pending |

Skipped: App. C–D (Monitors — marked "Deprecated" by the authors), App. G–H (project
assignment lists, not teaching material). Dialogue chapters are folded into the next teaching chapter.
