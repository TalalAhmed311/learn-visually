/* learn-visually — shared page behaviour (same for every book). No storage is required. */
(function () {
  "use strict";
  var LV = (window.LV = window.LV || {});
  var root = document.documentElement;
  root.classList.add("js");
  LV.reducedMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- theme toggle (storage optional) ---------- */
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var saved = store("lv-theme");
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function syncThemeBtn() {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
      b.setAttribute("aria-label", isDark() ? "Switch to light theme" : "Switch to dark theme");
      b.setAttribute("title", isDark() ? "Light theme" : "Dark theme");
      b.innerHTML = isDark()
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
    });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-theme-toggle]");
    if (!b) return;
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    store("lv-theme", next);
    syncThemeBtn();
    document.dispatchEvent(new CustomEvent("lv:theme"));
  });
  syncThemeBtn();

  /* ---------- reading progress ---------- */
  var bar = document.querySelector(".progress");
  function onScroll() {
    if (!bar) return;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + "%";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- TOC drawer + scrollspy ---------- */
  var toc = document.querySelector(".toc");
  var scrim = document.querySelector(".toc-scrim");
  var tocBtn = document.querySelector(".toc-toggle");
  function setToc(open) {
    if (!toc) return;
    toc.classList.toggle("open", open);
    if (scrim) scrim.classList.toggle("open", open);
    if (tocBtn) tocBtn.setAttribute("aria-expanded", String(open));
  }
  if (tocBtn) tocBtn.addEventListener("click", function () { setToc(!toc.classList.contains("open")); });
  if (scrim) scrim.addEventListener("click", function () { setToc(false); });
  if (toc) toc.addEventListener("click", function (e) { if (e.target.closest("a")) setToc(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setToc(false); });

  if (toc && "IntersectionObserver" in window) {
    var links = Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']"));
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      var current = null;
      for (var i = 0; i < links.length; i++) {
        var id = links[i].getAttribute("href").slice(1);
        if (visible[id]) { current = id; break; }
      }
      if (current) {
        links.forEach(function (a) { a.classList.remove("active"); a.removeAttribute("aria-current"); });
        map[current].classList.add("active");
        map[current].setAttribute("aria-current", "true");
      }
    }, { rootMargin: "-70px 0px -55% 0px" });
    Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) io.observe(el); });
  }

  /* ---------- code blocks: gutter, copy, annotation highlight ---------- */
  function copyText(text, btn) {
    function done(ok) { var o = btn.textContent; btn.textContent = ok ? "copied ✓" : "press Ctrl+C"; setTimeout(function () { btn.textContent = o; }, 1400); }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { fallback(); });
    } else fallback();
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); done(ok);
    }
  }
  document.querySelectorAll(".code").forEach(function (block) {
    var pre = block.querySelector("pre");
    var codeEl = pre && pre.querySelector("code");
    if (!pre || !codeEl) return;
    // strip a single leading newline left by the HTML source
    if (codeEl.firstChild && codeEl.firstChild.nodeType === 3) codeEl.firstChild.nodeValue = codeEl.firstChild.nodeValue.replace(/^\n/, "");
    var raw = codeEl.textContent.replace(/\n$/, "");
    var head = block.querySelector(".code-head");
    if (head && !head.querySelector(".copy-btn")) {
      var btn = document.createElement("button");
      btn.className = "copy-btn"; btn.type = "button"; btn.textContent = "copy";
      btn.setAttribute("aria-label", "Copy code to clipboard");
      btn.addEventListener("click", function () {
        var t = raw;
        if (block.classList.contains("term")) t = raw.split("\n").filter(function (l) { return /^\s*(\$|prompt>)\s/.test(l); }).map(function (l) { return l.replace(/^\s*(\$|prompt>)\s/, ""); }).join("\n") || raw;
        copyText(t, btn);
      });
      head.appendChild(btn);
    }
    var body = block.querySelector(".code-body");
    if (body && !block.classList.contains("no-gutter")) {
      var n = raw.split("\n").length;
      var g = document.createElement("div");
      g.className = "gutter"; g.setAttribute("aria-hidden", "true");
      for (var i = 1; i <= n; i++) { var s = document.createElement("span"); s.textContent = i; g.appendChild(s); }
      body.insertBefore(g, body.firstChild);
    }
  });
  function parseLines(spec) {
    var out = [];
    String(spec || "").split(",").forEach(function (part) {
      var m = part.trim().match(/^(\d+)(?:-(\d+))?$/);
      if (!m) return;
      for (var i = +m[1]; i <= +(m[2] || m[1]); i++) out.push(i);
    });
    return out;
  }
  function highlight(block, lines) {
    block.querySelectorAll(".line-hl").forEach(function (x) { x.remove(); });
    block.querySelectorAll(".gutter span.hl").forEach(function (x) { x.classList.remove("hl"); });
    if (!lines.length) return;
    var pre = block.querySelector("pre");
    var body = block.querySelector(".code-body");
    var lh = parseFloat(getComputedStyle(pre).lineHeight);
    var top = pre.offsetTop + parseFloat(getComputedStyle(pre).paddingTop);
    var spans = block.querySelectorAll(".gutter span");
    lines.forEach(function (ln) {
      var d = document.createElement("div");
      d.className = "line-hl";
      d.style.top = top + (ln - 1) * lh + "px";
      d.style.height = lh + "px";
      body.appendChild(d);
      if (spans[ln - 1]) spans[ln - 1].classList.add("hl");
    });
  }
  document.querySelectorAll(".annot[data-for]").forEach(function (list) {
    var block = document.getElementById(list.getAttribute("data-for"));
    if (!block) return;
    list.querySelectorAll("li[data-lines]").forEach(function (li) {
      li.tabIndex = 0;
      var lines = parseLines(li.getAttribute("data-lines"));
      function on() { li.classList.add("on"); highlight(block, lines); }
      function off() { li.classList.remove("on"); highlight(block, []); }
      li.addEventListener("mouseenter", on); li.addEventListener("mouseleave", off);
      li.addEventListener("focus", on); li.addEventListener("blur", off);
    });
  });

  /* ---------- quiz ---------- */
  document.querySelectorAll(".quiz").forEach(function (quiz) {
    var qs = quiz.querySelectorAll(".q");
    var scoreEl = quiz.querySelector(".score");
    var answered = 0, right = 0;
    function updateScore() {
      if (!scoreEl) return;
      scoreEl.textContent = answered === qs.length
        ? "Score: " + right + " / " + qs.length + (right === qs.length ? " — perfect. You're ready for the next chapter." : right >= qs.length - 2 ? " — solid. Re-read the explanations for the ones you missed." : " — worth another pass through the concepts above.")
        : "Answered " + answered + " / " + qs.length + " · correct so far: " + right;
    }
    qs.forEach(function (q) {
      var ans = q.getAttribute("data-answer");
      var fb = q.querySelector(".fb");
      q.addEventListener("change", function (e) {
        if (q._done || !e.target.matches("input[type=radio]")) return;
        q._done = true; answered++;
        var ok = e.target.value === ans;
        if (ok) right++;
        q.querySelectorAll("input[type=radio]").forEach(function (inp) {
          var lab = inp.closest("label");
          if (inp.value === ans) lab.classList.add("correct");
          else if (inp === e.target) lab.classList.add("incorrect");
          inp.disabled = true;
        });
        if (fb) {
          fb.classList.add("show", ok ? "good" : "bad");
          fb.insertAdjacentHTML("afterbegin", '<strong class="verdict">' + (ok ? "Correct. " : "Not quite. ") + "</strong>");
        }
        updateScore();
      });
    });
    var reset = quiz.querySelector("[data-quiz-reset]");
    if (reset) reset.addEventListener("click", function () {
      answered = 0; right = 0;
      qs.forEach(function (q) {
        q._done = false;
        q.querySelectorAll("label").forEach(function (l) { l.classList.remove("correct", "incorrect"); });
        q.querySelectorAll("input").forEach(function (i) { i.disabled = false; i.checked = false; });
        var fb = q.querySelector(".fb");
        if (fb) { fb.classList.remove("show", "good", "bad"); var v = fb.querySelector(".verdict"); if (v) v.remove(); }
      });
      updateScore();
    });
    updateScore();
  });

  /* ---------- glossary tooltips ---------- */
  var gloss = {};
  document.querySelectorAll(".glossary dt[id]").forEach(function (dt) {
    var dd = dt.nextElementSibling;
    if (dd) gloss[dt.id] = { term: dt.textContent.trim(), def: dd.textContent.trim() };
  });
  var tip = null;
  function showTip(el) {
    var key = el.getAttribute("data-term");
    var g = gloss["g-" + key];
    if (!g) return;
    hideTip();
    tip = document.createElement("div");
    tip.className = "tip"; tip.id = "lv-tip"; tip.setAttribute("role", "tooltip");
    tip.innerHTML = "<b></b><span></span>";
    tip.firstChild.textContent = g.term; tip.lastChild.textContent = g.def;
    document.body.appendChild(tip);
    el.setAttribute("aria-describedby", "lv-tip");
    var r = el.getBoundingClientRect();
    var tw = tip.offsetWidth, th = tip.offsetHeight;
    var left = Math.max(16, Math.min(window.scrollX + r.left + r.width / 2 - tw / 2, window.scrollX + document.documentElement.clientWidth - tw - 16));
    var top = window.scrollY + r.top - th - 8;
    if (r.top - th - 8 < 60) top = window.scrollY + r.bottom + 8;
    tip.style.left = left + "px"; tip.style.top = top + "px";
  }
  function hideTip() { if (tip) { tip.remove(); tip = null; } document.querySelectorAll(".gl[aria-describedby]").forEach(function (x) { x.removeAttribute("aria-describedby"); }); }
  document.querySelectorAll(".gl[data-term]").forEach(function (el) {
    if (!el.hasAttribute("tabindex")) el.tabIndex = 0;
    if (!el.getAttribute("href")) el.setAttribute("href", "#g-" + el.getAttribute("data-term"));
    el.addEventListener("mouseenter", function () { showTip(el); });
    el.addEventListener("mouseleave", hideTip);
    el.addEventListener("focus", function () { showTip(el); });
    el.addEventListener("blur", hideTip);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideTip(); });
  window.addEventListener("scroll", hideTip, { passive: true });

  /* ---------- drag-to-order exercises ---------- */
  document.querySelectorAll(".order-ex").forEach(function (ex) {
    var list = ex.querySelector(".order-list");
    var solution = (list.getAttribute("data-solution") || "").split(",");
    var status = ex.querySelector(".order-status");
    var dragged = null;
    function addMovers(li) {
      var mv = document.createElement("span");
      mv.className = "mv";
      mv.innerHTML = '<button type="button" class="btn" aria-label="Move up">↑</button><button type="button" class="btn" aria-label="Move down">↓</button>';
      mv.children[0].addEventListener("click", function () { if (li.previousElementSibling) list.insertBefore(li, li.previousElementSibling); clearMarks(); mv.children[0].focus(); });
      mv.children[1].addEventListener("click", function () { if (li.nextElementSibling) list.insertBefore(li.nextElementSibling, li); clearMarks(); mv.children[1].focus(); });
      li.appendChild(mv);
    }
    function clearMarks() { list.querySelectorAll("li").forEach(function (l) { l.classList.remove("correct", "wrong"); }); if (status) status.textContent = ""; }
    function shuffle() {
      var items = Array.prototype.slice.call(list.children);
      for (var tries = 0; tries < 20; tries++) {
        for (var i = items.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = items[i]; items[i] = items[j]; items[j] = t; }
        if (items.map(function (x) { return x.getAttribute("data-key"); }).join(",") !== solution.join(",")) break;
      }
      items.forEach(function (x) { list.appendChild(x); });
      clearMarks();
    }
    list.querySelectorAll("li").forEach(function (li) {
      li.draggable = true;
      addMovers(li);
      li.addEventListener("dragstart", function (e) { dragged = li; li.classList.add("dragging"); try { e.dataTransfer.setData("text/plain", ""); } catch (x) {} });
      li.addEventListener("dragend", function () { li.classList.remove("dragging"); dragged = null; clearMarks(); });
      li.addEventListener("dragover", function (e) {
        e.preventDefault();
        if (!dragged || dragged === li) return;
        var r = li.getBoundingClientRect();
        list.insertBefore(dragged, e.clientY > r.top + r.height / 2 ? li.nextSibling : li);
      });
    });
    var check = ex.querySelector("[data-order-check]");
    var again = ex.querySelector("[data-order-shuffle]");
    if (check) check.addEventListener("click", function () {
      var items = list.querySelectorAll("li"), ok = 0;
      items.forEach(function (li, i) { var good = li.getAttribute("data-key") === solution[i]; li.classList.toggle("correct", good); li.classList.toggle("wrong", !good); if (good) ok++; });
      if (status) status.textContent = ok === items.length ? "All " + ok + " steps in the right order. ✓" : ok + " / " + items.length + " in the right position. Green = correct spot.";
    });
    if (again) again.addEventListener("click", shuffle);
    shuffle();
  });

  /* ---------- print helpers ---------- */
  var reopened = [];
  window.addEventListener("beforeprint", function () {
    reopened = [];
    document.querySelectorAll("details:not([open])").forEach(function (d) { d.open = true; reopened.push(d); });
  });
  window.addEventListener("afterprint", function () {
    reopened.forEach(function (d) { d.open = false; });
    document.body.classList.remove("print-cheatsheet");
  });
  document.querySelectorAll("[data-print-cheatsheet]").forEach(function (b) {
    b.addEventListener("click", function () { document.body.classList.add("print-cheatsheet"); window.print(); });
  });

  /* ---------- motion: scroll reveal, spotlight, count-up, typing ---------- */
  var revealSel = "main > section.block > h2, main > section.block > p, .hero > *, .stats > *, .concept, .why-grid > .box, figure.viz, .lab, .box, .code, details, .takeaways > li, .exercise, .q, .cheatsheet, .glossary .g-item, .conn-grid > .box, .pager > *, .table-wrap, .annot, .cards > .card";
  var revealEls = Array.prototype.slice.call(document.querySelectorAll(revealSel));
  if ("IntersectionObserver" in window && !LV.reducedMotion) {
    var seen = 0;
    revealEls.forEach(function (el) {
      if (el.closest(".concept") && el !== el.closest(".concept") && !el.matches("figure.viz, .lab")) return; // concept children ride with the card
      el.classList.add("reveal");
      var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
      if (el.matches(".stats > *, .why-grid > .box, .takeaways > li, .glossary .g-item, .conn-grid > .box, .cards > .card, .hero > *")) el.style.setProperty("--d", Math.min(sib, 8) * 0.07 + "s");
    });
    var rio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); rio.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    document.querySelectorAll(".reveal").forEach(function (el) { rio.observe(el); });
    // figures that are not reveal targets still get flowing arrows when visible
    var fio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.target.classList.toggle("in", en.isIntersecting); });
    }, { threshold: 0.1 });
    document.querySelectorAll("figure.viz").forEach(function (f) { fio.observe(f); });
  } else {
    document.querySelectorAll("figure.viz").forEach(function (f) { if (!LV.reducedMotion) f.classList.add("in"); });
  }
  // pause SVG SMIL animations when the user prefers reduced motion
  if (LV.reducedMotion) document.querySelectorAll("svg").forEach(function (s) { if (s.pauseAnimations) s.pauseAnimations(); });

  // cursor spotlight on glass cards
  if (window.matchMedia && window.matchMedia("(hover: hover)").matches) {
    document.addEventListener("pointermove", function (e) {
      var el = e.target.closest && e.target.closest(".box, figure.viz, details, .exercise, .q, .card, .pager a");
      if (!el) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (e.clientX - r.left) + "px");
      el.style.setProperty("--my", (e.clientY - r.top) + "px");
    }, { passive: true });
  }

  // count-up numbers: <b data-count="9">9</b>
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = +el.getAttribute("data-count");
    if (LV.reducedMotion || !("IntersectionObserver" in window)) { el.textContent = target; return; }
    el.textContent = "0";
    var cio = new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting) return;
      cio.disconnect();
      var t0 = performance.now(), dur = 1100;
      (function tick(now) {
        var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(target * e);
        if (k < 1) requestAnimationFrame(tick);
      })(t0);
    });
    cio.observe(el);
  });

  // typing effect: <tspan data-type="text"> or <span data-type="text">
  document.querySelectorAll("[data-type]").forEach(function (el) {
    var full = el.getAttribute("data-type");
    if (LV.reducedMotion) { el.textContent = full; return; }
    var i = 0;
    el.textContent = "";
    (function type() {
      el.textContent = full.slice(0, ++i);
      if (i < full.length) setTimeout(type, 38 + Math.random() * 40);
      else setTimeout(function () { i = 0; type(); }, 5200);
    })();
  });

  /* ---------- tiny animation helper for labs ---------- */
  LV.player = function (opts) {
    // opts: { step(): bool (false when finished), interval(): ms, onState(playing) }
    var timer = null;
    function tick() { if (opts.step() === false) { stop(); return; } timer = setTimeout(tick, opts.interval()); }
    function play() { if (timer) return; opts.onState && opts.onState(true); timer = setTimeout(tick, LV.reducedMotion ? 0 : 10); }
    function stop() { if (timer) clearTimeout(timer); timer = null; opts.onState && opts.onState(false); }
    return { play: play, pause: stop, toggle: function () { timer ? stop() : play(); }, playing: function () { return !!timer; } };
  };
  LV.cssVar = function (name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); };
})();
