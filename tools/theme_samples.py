#!/usr/bin/env python3
"""Generate minimalist theme sample pages into docs/themes/."""
import pathlib

OUT = pathlib.Path("/home/user/learn-visually/docs/themes")
OUT.mkdir(parents=True, exist_ok=True)

CONTENT = """
<header class="top">
  <a href="index.html" class="back">← All themes</a>
  <button class="toggle" type="button" aria-label="Toggle dark mode">Dark / Light</button>
</header>
<main>
  <p class="eyebrow">Chapter 01 · Introduction</p>
  <h1>What is an Operating System?</h1>
  <p class="lead">The software that lets many programs share one machine — safely, and as if each had it to itself.</p>

  <h2>Key definitions</h2>
  <dl class="defs">
    <dt>Operating system</dt>
    <dd>Software that manages the hardware and offers programs a simpler, safer way to use it.</dd>
    <dt>Process</dt>
    <dd>A running program: its code, its memory, and the CPU state it needs to continue.</dd>
    <dt>Virtualization</dt>
    <dd>Making one physical resource look like many private ones — one CPU feels like many.</dd>
    <dt>System call</dt>
    <dd>A controlled request from a program to the OS, e.g. <code>open()</code> or <code>write()</code>.</dd>
  </dl>

  <h2>A tiny example</h2>
  <p>Writing to a file is a request to the OS. The program never touches the disk directly.</p>
  <pre class="code"><code><span class="k">int</span> fd = open(<span class="s">"notes.txt"</span>, O_WRONLY | O_CREAT, <span class="n">0644</span>);
write(fd, <span class="s">"hello\\n"</span>, <span class="n">6</span>);   <span class="c">// system call</span>
close(fd);</code></pre>

  <figure class="fig">
    <svg viewBox="0 0 520 190" role="img" aria-label="Layers: programs on top, the operating system in the middle, hardware at the bottom">
      <rect x="10" y="10" width="500" height="44" rx="6" class="l1"/>
      <text x="260" y="37" class="lt">Programs — browser, shell, your code</text>
      <rect x="10" y="72" width="500" height="44" rx="6" class="l2"/>
      <text x="260" y="99" class="lt">Operating system</text>
      <rect x="10" y="134" width="500" height="44" rx="6" class="l3"/>
      <text x="260" y="161" class="lt">Hardware — CPU, memory, disk</text>
    </svg>
    <figcaption>Programs reach the hardware only through the OS.</figcaption>
  </figure>

  <aside class="callout">
    <strong>Common mistake</strong>
    <p><code>printf</code> is not a system call. It is a library function that eventually calls <code>write()</code>.</p>
  </aside>

  <section class="quiz">
    <p class="q">Quick check: which of these is a system call?</p>
    <ol class="opts">
      <li><button type="button" data-ok="0">strlen()</button></li>
      <li><button type="button" data-ok="1">write()</button></li>
      <li><button type="button" data-ok="0">printf()</button></li>
    </ol>
    <p class="fb" aria-live="polite"></p>
  </section>

  <nav class="pager">
    <a href="#">← Previous</a>
    <a href="#">Next: The Process →</a>
  </nav>
</main>
<script>
document.querySelector(".toggle").addEventListener("click", function () {
  var r = document.documentElement;
  var dark = r.dataset.theme ? r.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  r.dataset.theme = dark ? "light" : "dark";
});
document.querySelectorAll(".opts button").forEach(function (b) {
  b.addEventListener("click", function () {
    document.querySelectorAll(".opts button").forEach(function (x) { x.classList.remove("right", "wrong"); });
    var ok = b.dataset.ok === "1";
    b.classList.add(ok ? "right" : "wrong");
    document.querySelector(".fb").textContent = ok ? "Correct — write() asks the kernel to do the work." : "Not quite — that one runs entirely inside your program.";
  });
});
</script>
"""

BASE = """
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);line-height:1.7;-webkit-font-smoothing:antialiased}
main{max-width:680px;margin:0 auto;padding:24px 20px 80px}
.top{max-width:680px;margin:0 auto;padding:18px 20px 0;display:flex;justify-content:space-between;align-items:center;font-size:.85rem}
.back{color:var(--muted);text-decoration:none} .back:hover{color:var(--accent)}
.toggle{font:inherit;font-size:.8rem;color:var(--muted);background:none;border:1px solid var(--line);border-radius:var(--r);padding:.3rem .7rem;cursor:pointer}
.toggle:hover{color:var(--fg)}
h1,h2{font-family:var(--head);color:var(--strong);line-height:1.2}
h1{font-size:clamp(2rem,5vw,2.6rem);margin:.2em 0 .3em;letter-spacing:-.02em}
h2{font-size:1.3rem;margin:2.4em 0 .6em}
.eyebrow{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:2rem 0 0}
.lead{font-size:1.15rem;color:var(--muted)}
code,pre{font-family:var(--mono)}
:not(pre)>code{font-size:.88em;background:var(--soft);padding:.1em .35em;border-radius:4px}
.defs{margin:0}
.defs dt{font-weight:600;color:var(--strong);margin-top:1rem}
.defs dd{margin:.15rem 0 0;color:var(--fg)}
.code{background:var(--codebg);color:var(--codefg);padding:1rem 1.2rem;border-radius:var(--r);overflow-x:auto;font-size:.85rem;line-height:1.6}
.code .k{color:var(--ck)} .code .s{color:var(--cs)} .code .n{color:var(--cn)} .code .c{color:var(--cc);font-style:italic}
.fig{margin:2rem 0}
.fig svg{width:100%;height:auto;display:block}
.fig figcaption{font-size:.85rem;color:var(--muted);margin-top:.5rem}
.l1,.l2,.l3{fill:var(--soft);stroke:var(--line)} .l2{fill:var(--accent-soft);stroke:var(--accent)}
.lt{font-family:var(--body);font-size:14px;fill:var(--strong);text-anchor:middle}
.callout{margin:2rem 0;padding:1rem 1.2rem;border-left:3px solid var(--accent);background:var(--soft);border-radius:0 var(--r) var(--r) 0}
.callout p{margin:.3rem 0 0}
.quiz{margin:2.5rem 0;padding-top:1.5rem;border-top:1px solid var(--line)}
.q{font-weight:600;color:var(--strong)}
.opts{list-style:none;padding:0;display:grid;gap:.5rem}
.opts button{width:100%;text-align:left;font:inherit;font-family:var(--mono);font-size:.9rem;color:var(--fg);background:transparent;border:1px solid var(--line);border-radius:var(--r);padding:.6rem .9rem;cursor:pointer}
.opts button:hover{border-color:var(--accent)}
.opts button.right{border-color:var(--ok);color:var(--ok)} .opts button.wrong{border-color:var(--bad);color:var(--bad)}
.fb{color:var(--muted);min-height:1.5em}
.pager{display:flex;justify-content:space-between;gap:1rem;margin-top:3rem;padding-top:1.2rem;border-top:1px solid var(--line);font-size:.92rem}
.pager a{color:var(--accent);text-decoration:none} .pager a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
"""

def tokens(light, dark):
    l = ";".join(f"--{k}:{v}" for k, v in light.items())
    d = ";".join(f"--{k}:{v}" for k, v in dark.items())
    return (f":root{{{l};color-scheme:light}}"
            f"@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{{d};color-scheme:dark}}}}"
            f":root[data-theme=dark]{{{d};color-scheme:dark}}")

THEMES = [
    dict(slug="paper", name="Paper", blurb="Warm off-white, serif headings, one ink-blue accent. Reads like a well-set textbook.",
         fonts="family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Inter:wght@400;600&family=JetBrains+Mono",
         common=dict(head='"Newsreader",Georgia,serif', body='"Inter",system-ui,sans-serif', mono='"JetBrains Mono",monospace', r="4px"),
         light=dict(bg="#faf8f4", fg="#2b2b2b", strong="#111", muted="#6b6760", line="#e4dfd6", soft="#f2eee7", accent="#1f4e8c", **{"accent-soft": "#e6edf6"},
                    codebg="#f2eee7", codefg="#2b2b2b", ck="#1f4e8c", cs="#7a4b00", cn="#8a2c2c", cc="#8a857c", ok="#2f6b3a", bad="#a12d2d"),
         dark=dict(bg="#1b1a18", fg="#d9d5cd", strong="#f3efe7", muted="#9a958c", line="#34312c", soft="#25231f", accent="#8db4e8", **{"accent-soft": "#22303f"},
                   codebg="#25231f", codefg="#d9d5cd", ck="#8db4e8", cs="#d9b27a", cn="#e09a9a", cc="#7d786f", ok="#8fc79a", bad="#e08b8b")),
    dict(slug="mono", name="Mono", blurb="Black and white with a single blue. Clean sans-serif, sharp corners, no decoration.",
         fonts="family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600",
         common=dict(head='"IBM Plex Sans",system-ui,sans-serif', body='"IBM Plex Sans",system-ui,sans-serif', mono='"IBM Plex Mono",monospace', r="0px"),
         light=dict(bg="#ffffff", fg="#222", strong="#000", muted="#666", line="#ddd", soft="#f5f5f5", accent="#0050d8", **{"accent-soft": "#eef3fd"},
                    codebg="#f5f5f5", codefg="#111", ck="#0050d8", cs="#222", cn="#0050d8", cc="#888", ok="#0a7d32", bad="#c4161c"),
         dark=dict(bg="#0d0d0d", fg="#d4d4d4", strong="#fff", muted="#8a8a8a", line="#2a2a2a", soft="#161616", accent="#6aa0ff", **{"accent-soft": "#121c2e"},
                   codebg="#161616", codefg="#e6e6e6", ck="#6aa0ff", cs="#e6e6e6", cn="#6aa0ff", cc="#6f6f6f", ok="#5cc77f", bad="#ff6b6b")),
    dict(slug="calm", name="Calm Dark", blurb="Dark-first graphite with soft gray text and a muted teal. Easy on the eyes at night.",
         fonts="family=Inter:wght@400;600;700&family=JetBrains+Mono",
         common=dict(head='"Inter",system-ui,sans-serif', body='"Inter",system-ui,sans-serif', mono='"JetBrains Mono",monospace', r="8px"),
         light=dict(bg="#f4f5f5", fg="#2c3333", strong="#111717", muted="#667070", line="#dde1e1", soft="#eaeded", accent="#2a7f7a", **{"accent-soft": "#e1efee"},
                    codebg="#1d2222", codefg="#d6dede", ck="#7fc8c2", cs="#c9d48f", cn="#e3b17d", cc="#6c7878", ok="#2a7f5a", bad="#b04646"),
         dark=dict(bg="#141818", fg="#c6cdcd", strong="#eef3f3", muted="#859090", line="#263030", soft="#1b2121", accent="#6cc0b8", **{"accent-soft": "#1a2b2a"},
                   codebg="#0f1313", codefg="#d6dede", ck="#7fc8c2", cs="#c9d48f", cn="#e3b17d", cc="#5d6969", ok="#7fcf9f", bad="#e38c8c"),
         force_dark=True),
    dict(slug="notes", name="Notes", blurb="Like a tidy notes app: system font, light gray blocks, gentle rounded corners, muted purple.",
         fonts="",
         common=dict(head='ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif', body='ui-sans-serif,-apple-system,"Segoe UI",Roboto,sans-serif', mono='ui-monospace,SFMono-Regular,Menlo,Consolas,monospace', r="10px"),
         light=dict(bg="#ffffff", fg="#37352f", strong="#191919", muted="#787774", line="#e9e9e7", soft="#f7f6f3", accent="#6b5bd2", **{"accent-soft": "#efedfb"},
                    codebg="#f7f6f3", codefg="#37352f", ck="#6b5bd2", cs="#0f7b6c", cn="#d9730d", cc="#9b9a97", ok="#0f7b6c", bad="#e03e3e"),
         dark=dict(bg="#191919", fg="#d4d4d2", strong="#f1f1ef", muted="#9b9b98", line="#2f2f2f", soft="#252525", accent="#a397f0", **{"accent-soft": "#2a2740"},
                   codebg="#252525", codefg="#e3e3e1", ck="#a397f0", cs="#4dab9a", cn="#ffa344", cc="#7f7f7c", ok="#4dab9a", bad="#ff7369")),
]

def page(t):
    css = tokens({**t["common"], **t["light"]}, {**t["common"], **t["dark"]}) + BASE
    fonts = (f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             f'<link href="https://fonts.googleapis.com/css2?{t["fonts"]}&display=swap" rel="stylesheet">') if t["fonts"] else ""
    attr = ' data-theme="dark"' if t.get("force_dark") else ""
    return (f'<!doctype html>\n<html lang="en"{attr}>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>Theme sample · {t["name"]}</title>\n{fonts}\n<style>{css}</style>\n</head>\n<body>{CONTENT}</body>\n</html>\n')

for t in THEMES:
    (OUT / f'{t["slug"]}.html').write_text(page(t))

cards = "".join(
    f'<a class="card" href="{t["slug"]}.html"><span class="sw">'
    + "".join(f'<i style="background:{c}"></i>' for c in (t["light"]["bg"], t["light"]["soft"], t["light"]["accent"], t["dark"]["bg"], t["dark"]["accent"]))
    + f'</span><strong>{t["name"]}</strong><span>{t["blurb"]}</span></a>'
    for t in THEMES)
index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Theme samples</title>
<style>
:root{{color-scheme:light dark;--bg:#fff;--fg:#222;--muted:#666;--line:#e5e5e5}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111;--fg:#ddd;--muted:#999;--line:#2a2a2a}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,sans-serif;line-height:1.6}}
main{{max-width:720px;margin:0 auto;padding:48px 20px}}
h1{{margin:0 0 .3em}} p{{color:var(--muted)}}
.grid{{display:grid;gap:12px;margin-top:24px}}
.card{{display:grid;gap:4px;padding:16px 18px;border:1px solid var(--line);border-radius:10px;color:inherit;text-decoration:none}}
.card:hover{{border-color:var(--fg)}}
.card span{{color:var(--muted);font-size:.92rem}}
.sw{{display:flex;gap:4px;margin-bottom:6px}} .sw i{{width:22px;height:22px;border-radius:5px;border:1px solid var(--line)}}
</style></head>
<body><main>
<h1>Pick a theme</h1>
<p>Same short sample content in four minimalist styles. Each page has a Dark / Light toggle in the top-right corner.</p>
<div class="grid">{cards}</div>
</main></body></html>
"""
(OUT / "index.html").write_text(index)
print("wrote", sorted(p.name for p in OUT.iterdir()))
