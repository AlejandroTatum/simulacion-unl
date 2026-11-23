/* Demo en vivo de aceptación-rechazo (Beta(2,2), propuesta uniforme), diapositivas 29 a 32.
   Corre el mismo algoritmo que codigo/beta22.py con el mismo generador (pcg64.js =
   numpy.random.default_rng(42)), así que al llegar a 10 000 muestras da los mismos
   números que Python. Un solo estado compartido: lo que corre en la 29 se ve en la 30, la 31 y la 32.
   Controles: botones Iniciar / Pausa / Reiniciar y M; teclado S (iniciar/pausar), R (reiniciar),
   1-4 (M = 1.5, 2, 3, 6) cuando la diapositiva activa tiene una demo.
   En ?print (PDF) no anima: dibuja la corrida completa y escribe los valores de Python
   (resultados.js, generado por codigo/beta22.py). */
"use strict";
(function () {
  const N = 10000, SEED = 42, BINS = 20, MAX_POINTS = 4000;
  const M_VALUES = [1.5, 2, 3, 6];
  const IS_PRINT = typeof PRINT !== "undefined" && PRINT;
  const PY = window.PY_RESULTS || null;
  const root = getComputedStyle(document.documentElement);
  const C = {
    f: root.getPropertyValue("--a1").trim() || "#E4572E",
    g: root.getPropertyValue("--a2").trim() || "#1F9E8F",
    m: root.getPropertyValue("--a3").trim() || "#6C4FD1",
    fg: root.getPropertyValue("--fg").trim() || "#1B1B1F",
    muted: root.getPropertyValue("--muted").trim() || "#6A665E",
    mono: root.getPropertyValue("--mono").trim() || "monospace",
  };

  // Densidad objetivo, igual que beta_22 en Python.
  const beta22 = (x) => (x >= 0 && x <= 1 ? 6 * x * (1 - x) : 0);

  function makeRun(m) {
    return { m, rng: createNumpyRng(SEED), acc: 0, att: 0, sum: 0, sum2: 0, bins: new Array(BINS).fill(0), pts: [], done: false };
  }

  // Un intento: candidato Y ~ g = U(0,1), umbral U ~ U(0,1), aceptar si U <= f(Y)/M.
  function attempt(run) {
    const y = run.rng.uniform();
    const u = run.rng.uniform();
    run.att += 1;
    const ok = u <= beta22(y) / run.m;
    if (ok) {
      run.acc += 1; run.sum += y; run.sum2 += y * y;
      run.bins[Math.min(BINS - 1, Math.floor(y * BINS))] += 1;
    }
    if (run.pts.length < MAX_POINTS) run.pts.push([y, u * run.m, ok]);
    if (run.acc >= N) run.done = true;
  }

  const stats = (run) => {
    const mean = run.acc ? run.sum / run.acc : NaN;
    return { mean, variance: run.acc ? run.sum2 / run.acc - mean * mean : NaN, eff: run.att ? run.acc / run.att : NaN };
  };

  // Formato del borrador: 10 000 (espacio de miles), punto decimal.
  const int = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " ");
  const pct = (v) => (isFinite(v) ? (v * 100).toFixed(2) + " %" : "—");
  const dec = (v) => (isFinite(v) ? v.toFixed(4) : "—");
  const mLabel = (m) => String(m);

  /* ---------- dibujo ---------- */
  function sizeCanvas(cv) {
    const w = Math.max(1, cv.offsetWidth), h = Math.max(1, cv.offsetHeight);
    if (cv.width !== w * 2 || cv.height !== h * 2) { cv.width = w * 2; cv.height = h * 2; }
    const ctx = cv.getContext("2d");
    ctx.setTransform(2, 0, 0, 2, 0, 0);
    return { ctx, w, h };
  }

  const PAD = { l: 90, r: 30, t: 30, b: 64 };

  function scatterFrame(view, run) {
    const { ctx, w, h } = sizeCanvas(view.ovl);
    ctx.clearRect(0, 0, w, h);
    const ymax = run.m * 1.12;
    const X = (x) => PAD.l + x * (w - PAD.l - PAD.r), Y = (v) => h - PAD.b - (v / ymax) * (h - PAD.t - PAD.b);
    // ejes
    ctx.strokeStyle = C.muted; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(1), Y(0)); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(ymax)); ctx.stroke();
    ctx.fillStyle = C.muted; ctx.font = "600 24px " + C.mono; ctx.textAlign = "center"; ctx.textBaseline = "top";
    [0, 0.5, 1].forEach((t) => ctx.fillText(String(t), X(t), Y(0) + 12));
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    ctx.fillText("0", X(0) - 14, Y(0));
    ctx.fillText("1.5", X(0) - 14, Y(1.5));
    if (run.m !== 1.5) ctx.fillText(mLabel(run.m), X(0) - 14, Y(run.m));
    // envolvente M·g
    ctx.strokeStyle = C.m; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(X(0), Y(run.m)); ctx.lineTo(X(1), Y(run.m)); ctx.stroke();
    ctx.fillStyle = C.m; ctx.font = "700 28px " + C.mono; ctx.textAlign = "right"; ctx.textBaseline = "bottom";
    ctx.fillText("M·g(x) = " + mLabel(run.m), X(1) - 6, Y(run.m) - 8);
    // densidad objetivo f
    ctx.strokeStyle = C.f; ctx.lineWidth = 6; ctx.beginPath();
    for (let i = 0; i <= 100; i++) { const x = i / 100; i ? ctx.lineTo(X(x), Y(beta22(x))) : ctx.moveTo(X(x), Y(beta22(x))); }
    ctx.stroke();
    ctx.fillStyle = C.f; ctx.textAlign = "left"; ctx.textBaseline = "bottom";
    ctx.fillText("f(x)", X(0.5) + 16, Y(1.5) - 6);
    return { X, Y };
  }

  function drawScatter(view, run) {
    const { X, Y } = scatterFrame(view, run);
    const { ctx } = sizeCanvas(view.pts);
    if (view.drawnFor !== run || view.drawnM !== run.m || view.drawn > run.pts.length) {
      ctx.clearRect(0, 0, view.pts.width, view.pts.height); view.drawn = 0; view.drawnFor = run; view.drawnM = run.m;
    }
    for (let i = view.drawn; i < run.pts.length; i++) {
      const [x, v, ok] = run.pts[i];
      ctx.beginPath(); ctx.arc(X(x), Y(v), ok ? 4.5 : 4, 0, Math.PI * 2);
      if (ok) { ctx.fillStyle = C.f; ctx.globalAlpha = 0.75; ctx.fill(); }
      else { ctx.strokeStyle = C.muted; ctx.globalAlpha = 0.55; ctx.lineWidth = 1.6; ctx.stroke(); }
    }
    ctx.globalAlpha = 1;
    view.drawn = run.pts.length;
  }

  function drawHistogram(view, run, fixedDensity) {
    const { ctx, w, h } = sizeCanvas(view.ovl);
    ctx.clearRect(0, 0, w, h);
    const ymax = 1.8;
    const X = (x) => PAD.l + x * (w - PAD.l - PAD.r), Y = (v) => h - PAD.b - (v / ymax) * (h - PAD.t - PAD.b);
    const dens = fixedDensity || run.bins.map((c) => (run.acc ? (c * BINS) / run.acc : 0));
    ctx.fillStyle = C.f; ctx.globalAlpha = 0.28;
    dens.forEach((d, i) => { const x0 = X(i / BINS) + 2, x1 = X((i + 1) / BINS) - 2; ctx.fillRect(x0, Y(Math.min(d, ymax)), x1 - x0, Y(0) - Y(Math.min(d, ymax))); });
    ctx.globalAlpha = 1;
    ctx.strokeStyle = C.muted; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(1), Y(0)); ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(ymax)); ctx.stroke();
    ctx.setLineDash([8, 10]); ctx.beginPath(); [0.5, 1, 1.5].forEach((v) => { ctx.moveTo(X(0), Y(v)); ctx.lineTo(X(1), Y(v)); }); ctx.globalAlpha = 0.35; ctx.stroke();
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    ctx.fillStyle = C.muted; ctx.font = "600 24px " + C.mono; ctx.textAlign = "center"; ctx.textBaseline = "top";
    [0, 0.25, 0.5, 0.75, 1].forEach((t) => ctx.fillText(String(t), X(t), Y(0) + 12));
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    [0, 0.5, 1, 1.5].forEach((v) => ctx.fillText(String(v), X(0) - 14, Y(v)));
    ctx.strokeStyle = C.f; ctx.lineWidth = 7; ctx.beginPath();
    for (let i = 0; i <= 120; i++) { const x = i / 120; i ? ctx.lineTo(X(x), Y(beta22(x))) : ctx.moveTo(X(x), Y(beta22(x))); }
    ctx.stroke();
    ctx.fillStyle = C.f; ctx.font = "700 30px " + C.mono; ctx.textAlign = "left"; ctx.textBaseline = "bottom";
    ctx.fillText("f(x) = 6x(1−x)", X(0.62), Y(1.62));
  }

  /* ---------- estado compartido en pantalla ---------- */
  let run = makeRun(1.5);
  let running = false;
  const best = {}; // última corrida completa por M: { eff, att }
  const views = [...document.querySelectorAll(".ar-plot")].map((el) => ({
    el, kind: el.dataset.view, pts: el.querySelector("canvas.ar-pts"), ovl: el.querySelector("canvas.ar-ovl"), drawn: 0,
  }));
  const setText = (key, value) => document.querySelectorAll('[data-ar="' + key + '"]').forEach((el) => { el.textContent = value; });

  function paintNumbers(r, s) {
    setText("acc", int(r.acc)); setText("rej", int(r.att - r.acc)); setText("att", int(r.att));
    setText("eff", pct(s.eff)); setText("mean", dec(s.mean)); setText("var", dec(s.variance));
    setText("m", mLabel(r.m)); setText("inv-m", pct(1 / r.m)); setText("nm", int(Math.round(N * r.m)));
  }

  function paintRows(current) {
    document.querySelectorAll(".ar-mrow").forEach((row) => {
      const m = Number(row.dataset.m);
      const live = current && current.m === m ? { eff: current.att ? current.acc / current.att : NaN, att: current.att } : null;
      const shown = live || best[m];
      row.classList.toggle("on", !!current && current.m === m);
      const obs = row.querySelector(".ar-fill.obs");
      if (obs) obs.style.setProperty("--v", shown && isFinite(shown.eff) ? (shown.eff * 100).toFixed(2) : 0);
      const ev = row.querySelector('[data-ar-row="eff"]'); if (ev) ev.textContent = shown ? pct(shown.eff) : "—";
      const av = row.querySelector('[data-ar-row="att"]'); if (av) av.textContent = shown ? int(shown.att) : "—";
    });
    document.querySelectorAll("[data-ar-m]").forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.arM) === run.m)));
  }

  function status() {
    if (run.done) {
      const py = PY && PY.corridas.find((c) => c.m === run.m);
      const same = py && py.intentos === run.att && py.aceptadas === run.acc;
      return "listo: " + int(N) + " muestras" + (py ? (same ? " · igual que Python ✓" : " · distinto de Python") : "");
    }
    return running ? "corriendo…" : run.att ? "en pausa" : "listo para iniciar";
  }

  function render() {
    views.forEach((v) => (v.kind === "hist" ? drawHistogram(v, run) : drawScatter(v, run)));
    paintNumbers(run, stats(run));
    paintRows(run);
    setText("status", status());
  }

  function frame() {
    if (!running) return;
    // Empieza lento para ver cada punto y acelera hasta completar las 10 000 muestras.
    const batch = Math.min(900, 1 + Math.floor(run.att / 30));
    for (let i = 0; i < batch && !run.done; i++) attempt(run);
    if (run.done) { running = false; best[run.m] = { eff: run.acc / run.att, att: run.att }; }
    render();
    if (running) requestAnimationFrame(frame);
  }

  const start = () => { if (run.done) run = makeRun(run.m); if (!running) { running = true; requestAnimationFrame(frame); } render(); };
  const pause = () => { running = false; render(); };
  const reset = (m) => { running = false; run = makeRun(m === undefined ? run.m : m); render(); };

  function screenInit() {
    render();
    document.addEventListener("click", (event) => {
      const btn = event.target.closest("[data-ar-act], [data-ar-m]");
      if (!btn) return;
      btn.blur();
      if (btn.dataset.arM) { reset(Number(btn.dataset.arM)); start(); return; }
      ({ start, pause, reset: () => reset() })[btn.dataset.arAct]();
    });
    document.addEventListener("keydown", (event) => {
      const active = document.querySelector(".slide.active");
      if (!active || !active.querySelector(".ar-demo")) return;
      const k = event.key.toLowerCase();
      if (k === "s") running ? pause() : start();
      else if (k === "r") reset();
      else if (["1", "2", "3", "4"].includes(k)) { reset(M_VALUES[Number(k) - 1]); start(); }
    });
    addEventListener("resize", render);
  }

  /* ---------- versión estática (PDF): corrida completa + valores de Python ---------- */
  function printInit() {
    const full = (m) => { const r = makeRun(m); while (!r.done) attempt(r); return r; };
    const r15 = full(1.5), r6 = full(6);
    views.forEach((v) => {
      const slideRun = v.el.closest(".ar-m-run") ? r6 : r15;
      if (v.kind === "hist") drawHistogram(v, r15, PY ? PY.corridas[0].histograma : null);
      else drawScatter(v, slideRun);
    });
    paintNumbers(r15, stats(r15));
    if (PY) {
      const p = PY.corridas[0];
      setText("acc", int(p.aceptadas)); setText("rej", int(p.rechazadas)); setText("att", int(p.intentos));
      setText("eff", pct(p.eficiencia)); setText("mean", dec(p.media)); setText("var", dec(p.varianza));
      PY.corridas.forEach((c) => { best[c.m] = { eff: c.eficiencia, att: c.intentos }; });
      if (r15.att !== p.intentos || r6.att !== PY.corridas[3].intentos) console.warn("ar-demo: la corrida JS no coincide con Python");
    }
    paintRows(null);
    document.querySelectorAll("[data-ar-m]").forEach((b) => b.setAttribute("aria-pressed", "false"));
  }

  const go = () => (IS_PRINT ? printInit() : screenInit());
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(go);
})();
