#!/usr/bin/env python3
"""Generate src/index.html (library home) and src/ostep/index.html (book index).

A chapter card links to its page only if docs/ostep/chapter-NN.html exists;
otherwise it is shown as "coming soon". Re-run after adding chapters, then
run tools/build.py.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, DOCS = ROOT / "src", ROOT / "docs"

# (study no., book chapters, title, summary, level, minutes)
OSTEP = [
    ("Introduction", [
        (1, "1–2", "Introduction to Operating Systems", "What an OS is and the three easy pieces: virtualization, concurrency, persistence.", "Beginner", 30),
    ]),
    ("Part I · Virtualization", [
        (2, "3–4", "The Abstraction: The Process", "What a process is, its machine state, states and the PCB.", "Beginner", 30),
        (3, "5", "Interlude: Process API", "fork(), exec() and wait(), and why UNIX splits them.", "Beginner", 30),
        (4, "6", "Limited Direct Execution", "Traps, timer interrupts and the context switch.", "Intermediate", 30),
        (5, "7", "Scheduling: Introduction", "FIFO, SJF, STCF, round robin; turnaround vs response time.", "Intermediate", 30),
        (6, "8", "Scheduling: The Multi-Level Feedback Queue", "Learning job behaviour without an oracle.", "Intermediate", 30),
        (7, "9", "Scheduling: Proportional Share", "Lottery and stride scheduling.", "Intermediate", 25),
        (8, "10–11", "Multiprocessor Scheduling", "Cache affinity, single vs multi-queue schedulers.", "Advanced", 30),
        (9, "12–13", "The Abstraction: Address Spaces", "Why every process gets its own view of memory.", "Beginner", 25),
        (10, "14", "Interlude: Memory API", "malloc, free and the classic memory bugs.", "Beginner", 25),
        (11, "15", "Mechanism: Address Translation", "Base and bounds, the MMU.", "Intermediate", 30),
        (12, "16", "Segmentation", "Generalized base/bounds and fragmentation.", "Intermediate", 25),
        (13, "17", "Free-Space Management", "Splitting, coalescing, fits, buddy allocation.", "Intermediate", 30),
        (14, "18", "Paging: Introduction", "Pages, page tables and translation.", "Intermediate", 30),
        (15, "19", "Paging: Faster Translations (TLBs)", "Caching translations in hardware.", "Intermediate", 30),
        (16, "20", "Paging: Smaller Tables", "Multi-level and inverted page tables.", "Advanced", 30),
        (17, "21", "Beyond Physical Memory: Mechanisms", "Swap space, the present bit, page faults.", "Intermediate", 25),
        (18, "22", "Beyond Physical Memory: Policies", "Optimal, FIFO, LRU, clock; thrashing.", "Intermediate", 30),
        (19, "23–24", "The VAX/VMS Virtual Memory System", "A complete real VM system.", "Advanced", 25),
    ]),
    ("Part II · Concurrency", [
        (20, "25–26", "Concurrency: An Introduction", "Threads, races, critical sections, atomicity.", "Intermediate", 30),
        (21, "27", "Interlude: Thread API", "pthread create/join, mutexes, condition variables.", "Beginner", 25),
        (22, "28", "Locks", "Spin locks, ticket locks, futexes.", "Advanced", 35),
        (23, "29", "Lock-based Concurrent Data Structures", "Counters, lists, queues, hash tables.", "Intermediate", 30),
        (24, "30", "Condition Variables", "Producer/consumer and Mesa semantics.", "Intermediate", 30),
        (25, "31", "Semaphores", "One primitive for locks and ordering.", "Intermediate", 30),
        (26, "32", "Common Concurrency Problems", "Atomicity and order violations, deadlock.", "Intermediate", 30),
        (27, "33–34", "Event-based Concurrency", "Event loops, select/poll, async I/O.", "Advanced", 25),
    ]),
    ("Part III · Persistence", [
        (28, "35–36", "I/O Devices", "Polling, interrupts, DMA, device drivers.", "Intermediate", 25),
        (29, "37", "Hard Disk Drives", "Seek, rotation, transfer; disk scheduling.", "Intermediate", 30),
        (30, "38", "RAID", "Striping, mirroring, parity.", "Intermediate", 30),
        (31, "39", "Interlude: Files and Directories", "The file-system API, links, mounting.", "Beginner", 30),
        (32, "40", "File System Implementation", "Inodes, bitmaps and access paths.", "Intermediate", 30),
        (33, "41", "Locality and the Fast File System", "Cylinder groups and placement.", "Intermediate", 25),
        (34, "42", "Crash Consistency: FSCK and Journaling", "Surviving crashes mid-update.", "Advanced", 30),
        (35, "43", "Log-structured File Systems", "Write everything sequentially.", "Advanced", 30),
        (36, "44–45", "Data Integrity and Protection", "Checksums, misdirected and lost writes.", "Intermediate", 25),
        (37, "46–47", "Distributed Systems", "Messages, reliability, RPC.", "Intermediate", 25),
        (38, "48", "Sun's Network File System (NFS)", "Statelessness and idempotency.", "Intermediate", 25),
        (39, "49–50", "The Andrew File System (AFS)", "Whole-file caching and callbacks.", "Intermediate", 25),
    ]),
    ("Appendices", [
        (40, "A–B", "Virtual Machine Monitors", "Virtualizing the OS itself.", "Advanced", 25),
        (41, "I", "Flash-based SSDs", "Erase blocks, FTLs, wear leveling.", "Advanced", 30),
        (42, "E–F", "Lab Tutorial: The C Development Environment", "Compiling, make, gdb, man pages.", "Beginner", 20),
    ]),
]

HEAD = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>/*@include shared/base.css*/
/*@include ostep/theme.css*/
main.wide {{ max-width: 980px; margin: 0 auto; padding: 0 20px 4rem; }}
.search {{ display: flex; flex-wrap: wrap; gap: .6rem; margin: 1.4rem 0 .4rem; }}
.search input {{ flex: 1 1 240px; }}
.tagchip {{ font-size: .74rem; color: var(--accent); }}
.empty {{ color: var(--muted); display: none; }}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
  <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle theme"></button>
  <div class="progress" aria-hidden="true"></div>
</header>
<main id="main" class="wide">
"""

FOOT = """</main>
<footer class="site">learn-visually · study guides built from the books in this repository.</footer>
<script>/*@include shared/base.js*/</script>
{extra}
</body>
</html>
"""


def esc(s):
    return html.escape(s, quote=True)


def book_index():
    built = {n for _, chs in OSTEP for (n, *_rest) in chs if (DOCS / "ostep" / f"chapter-{n:02d}.html").exists()}
    total = sum(len(c) for _, c in OSTEP)
    parts = []
    for part, chs in OSTEP:
        cards = []
        for n, book, title, summary, level, mins in chs:
            inner = (f'<span class="num">Ch. {n:02d} · book ch. {book}</span><h3>{esc(title)}</h3>'
                     f'<p>{esc(summary)}</p><div class="meta"><span class="chip level">{level}</span><span class="chip">~{mins} min</span></div>')
            if n in built:
                cards.append(f'<a class="card" href="chapter-{n:02d}.html">{inner}</a>')
            else:
                cards.append(f'<div class="card locked" aria-disabled="true">{inner}<span class="soon" style="font-size:.8rem">Not built yet</span></div>')
        parts.append(f'<h2 class="part-head">{esc(part)} <small>{len(chs)} chapter{"s" if len(chs) != 1 else ""}</small></h2>\n<div class="cards">{"".join(cards)}</div>')

    body = HEAD.format(
        title="Operating Systems: Three Easy Pieces — Study Guide",
        desc="Chapter-by-chapter visual study guide for Operating Systems: Three Easy Pieces.",
        crumbs='<a href="../index.html">library</a><span class="sep">/</span><span class="here">ostep</span>',
    ) + f"""
<header class="hero">
  <div class="kicker">Book · {len(built)} of {total} chapters ready</div>
  <h1>Operating Systems: Three Easy Pieces</h1>
  <p class="hook">Remzi H. Arpaci-Dusseau &amp; Andrea C. Arpaci-Dusseau · version 0.90/0.91 (© 2014)</p>
</header>

<section class="block" id="learn">
  <h2>What you'll learn</h2>
  <p>How an operating system works, built up from three ideas:</p>
  <ul>
    <li><strong>Virtualization</strong> — turning one CPU and one memory into many private ones: processes, scheduling, address spaces, paging.</li>
    <li><strong>Concurrency</strong> — running many things at once correctly: threads, locks, condition variables, semaphores.</li>
    <li><strong>Persistence</strong> — keeping data safe on devices that fail: disks, RAID, file systems, crash consistency, distributed file systems.</li>
  </ul>
  <p><strong>Prerequisites:</strong> basic C (pointers, <code>malloc</code>, structs), a rough idea of what a CPU, RAM and disk do, and comfort with a Unix shell.</p>
</section>

<section class="block" id="map">
  <h2>How the parts connect</h2>
  <figure class="viz">
    <div class="scroll-x">
    <svg viewBox="0 0 760 250" role="img" aria-labelledby="bm-t bm-d" style="min-width:560px">
      <title id="bm-t">Concept dependency map of the book</title>
      <desc id="bm-d">The introduction leads into three parts. Virtualization covers processes, then CPU scheduling, and address spaces, then paging and swapping. Concurrency covers threads, then locks, then condition variables and semaphores, then concurrency bugs and event-based concurrency. Persistence covers I/O devices and disks, then RAID, files and directories, then file-system implementation, then crash consistency, log-structured file systems and distributed file systems. Concurrency builds on virtualization, and persistence uses both.</desc>
      <defs><marker id="bma" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" class="f-muted"/></marker></defs>
      <rect x="280" y="8" width="200" height="40" rx="8" class="s-box"/><text x="380" y="33" text-anchor="middle" class="s-head">Introduction (Ch. 01)</text>
      <path d="M330 48 L 140 78M380 48v30M430 48 L 620 78" class="s-arrow" marker-end="url(#bma)"/>
      <rect x="20" y="80" width="240" height="160" rx="8" class="s-user"/>
      <text x="140" y="104" text-anchor="middle" class="s-head">Virtualization</text>
      <text x="140" y="130" text-anchor="middle" class="s-text">processes → scheduling</text>
      <text x="140" y="152" text-anchor="middle" class="s-text-soft">Ch. 02–08</text>
      <text x="140" y="182" text-anchor="middle" class="s-text">address spaces → paging</text>
      <text x="140" y="204" text-anchor="middle" class="s-text">→ swapping</text>
      <text x="140" y="226" text-anchor="middle" class="s-text-soft">Ch. 09–19</text>
      <rect x="270" y="80" width="220" height="160" rx="8" class="s-danger"/>
      <text x="380" y="104" text-anchor="middle" class="s-head">Concurrency</text>
      <text x="380" y="130" text-anchor="middle" class="s-text">threads → locks</text>
      <text x="380" y="152" text-anchor="middle" class="s-text">→ condition variables</text>
      <text x="380" y="174" text-anchor="middle" class="s-text">→ semaphores → bugs</text>
      <text x="380" y="196" text-anchor="middle" class="s-text">→ event-based</text>
      <text x="380" y="226" text-anchor="middle" class="s-text-soft">Ch. 20–27</text>
      <rect x="500" y="80" width="240" height="160" rx="8" class="s-violet"/>
      <text x="620" y="104" text-anchor="middle" class="s-head">Persistence</text>
      <text x="620" y="130" text-anchor="middle" class="s-text">devices → disks → RAID</text>
      <text x="620" y="152" text-anchor="middle" class="s-text">files → FS implementation</text>
      <text x="620" y="174" text-anchor="middle" class="s-text">→ FFS · journaling · LFS</text>
      <text x="620" y="196" text-anchor="middle" class="s-text">→ NFS · AFS</text>
      <text x="620" y="226" text-anchor="middle" class="s-text-soft">Ch. 28–39</text>
    </svg>
    </div>
    <figcaption><strong>Figure.</strong> Read the parts in order: concurrency builds on processes and address spaces, and persistence uses ideas from both.</figcaption>
  </figure>
</section>

<section class="block" id="chapters">
  <h2>Chapters</h2>
  {"".join(parts)}
</section>
""" + FOOT.format(extra="")
    (SRC / "ostep" / "index.html").write_text(body, encoding="utf-8")


BOOKS = [
    dict(href="ostep/index.html", title="Operating Systems: Three Easy Pieces", author="Remzi H. & Andrea C. Arpaci-Dusseau",
         topic="Operating systems", chapters=42, ready=None, blurb="Virtualization, concurrency and persistence — how an OS really works."),
    dict(href=None, title="Inside the Machine", author="Jon Stokes",
         topic="Computer architecture", chapters=12, ready=0, blurb="An illustrated introduction to microprocessors and computer architecture."),
    dict(href=None, title="Inference Engineering", author="Philip Kiely",
         topic="Machine learning", chapters=8, ready=0, blurb="Serving models in production: hardware, software, techniques and operations."),
]


def library_index():
    ostep_ready = len(list((DOCS / "ostep").glob("chapter-*.html")))
    cards = []
    for b in BOOKS:
        ready = ostep_ready if b["ready"] is None else b["ready"]
        inner = (f'<span class="tagchip">{esc(b["topic"])}</span><h3>{esc(b["title"])}</h3><p>{esc(b["author"])}</p>'
                 f'<p>{esc(b["blurb"])}</p><div class="meta"><span class="chip">{b["chapters"]} chapters</span><span class="chip">{ready} ready</span></div>')
        attrs = f'data-topic="{esc(b["topic"])}" data-text="{esc((b["title"] + " " + b["author"] + " " + b["topic"]).lower())}"'
        if b["href"]:
            cards.append(f'<a class="card book" {attrs} href="{b["href"]}">{inner}</a>')
        else:
            cards.append(f'<div class="card book locked" {attrs}>{inner}<span class="soon" style="font-size:.8rem">Not started</span></div>')
    topics = sorted({b["topic"] for b in BOOKS})
    options = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in topics)
    script = """<script>
(function () {
  var q = document.getElementById("q"), t = document.getElementById("topic"), empty = document.querySelector(".empty");
  function filter() {
    var s = q.value.trim().toLowerCase(), topic = t.value, shown = 0;
    document.querySelectorAll(".book").forEach(function (c) {
      var ok = (!s || c.getAttribute("data-text").indexOf(s) >= 0) && (!topic || c.getAttribute("data-topic") === topic);
      c.hidden = !ok; if (ok) shown++;
    });
    empty.style.display = shown ? "none" : "block";
  }
  q.addEventListener("input", filter); t.addEventListener("change", filter);
})();
</script>"""
    body = HEAD.format(
        title="Library — learn-visually",
        desc="Visual, chapter-by-chapter study guides for technical books.",
        crumbs='<span class="here">library</span>',
    ) + f"""
<header class="hero">
  <div class="kicker">learn-visually</div>
  <h1>Library</h1>
  <p class="hook">Chapter-by-chapter study pages with diagrams, runnable code, labs and quizzes.</p>
</header>
<div class="search" role="search">
  <input type="search" id="q" placeholder="Search by title, author or topic" aria-label="Search books">
  <select id="topic" aria-label="Filter by topic"><option value="">All topics</option>{options}</select>
</div>
<div class="cards">{"".join(cards)}</div>
<p class="empty">No books match.</p>
""" + FOOT.format(extra=script)
    (SRC / "index.html").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    book_index()
    library_index()
    print("wrote src/index.html and src/ostep/index.html")
