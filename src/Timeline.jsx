import { useEffect, useMemo, useRef, useState } from 'react';
import { fmtYear, fmtSpan } from './years.js';

// items: { id, lane, year, yearEnd?, title, summary?, meta?, color }
// lanes: [{ id, label, color }]
const LANE_H = 54;
const TOP = 34;
const LABEL_W = 150;

function niceStep(span) {
  const raw = span / 9;
  const p = 10 ** Math.floor(Math.log10(raw));
  for (const m of [1, 2, 2.5, 5, 10]) if (raw <= m * p) return m * p;
  return 10 * p;
}

export default function Timeline({ items, lanes, nowYear, cycle, initial = [-4200, 2300], onPick, picked }) {
  const wrap = useRef(null);
  const [size, setSize] = useState({ w: 1200, h: 500 });
  const [view, setView] = useState({ a: initial[0], b: initial[1] });
  const drag = useRef(null);
  const [dragging, setDragging] = useState(false);

  useEffect(() => {
    const el = wrap.current;
    const ro = new ResizeObserver(([e]) => setSize({ w: e.contentRect.width, h: e.contentRect.height }));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // Wheel zoom around the cursor; needs a non-passive listener to block page scroll.
  useEffect(() => {
    const el = wrap.current;
    const onWheel = (e) => {
      e.preventDefault();
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - LABEL_W;
      setView((v) => {
        const plotW = rect.width - LABEL_W;
        const at = v.a + (x / plotW) * (v.b - v.a);
        const k = Math.exp(e.deltaY * 0.0015);
        const span = Math.min(Math.max((v.b - v.a) * k, 6), 40000);
        const f = (at - v.a) / (v.b - v.a);
        return { a: at - f * span, b: at + (1 - f) * span };
      });
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, []);

  const plotW = Math.max(size.w - LABEL_W, 100);
  const x = (y) => LABEL_W + ((y - view.a) / (view.b - view.a)) * plotW;

  const ticks = useMemo(() => {
    // Tick on round historical years (4000 BC, 1000 AD) and convert to astronomical positions.
    const step = niceStep(view.b - view.a);
    const out = [];
    const ha = view.a <= 0 ? view.a - 1 : view.a;
    for (let h = Math.ceil(ha / step) * step; ; h += step) {
      const t = h < 0 ? h + 1 : h === 0 ? 1 : h;
      if (t > view.b) break;
      if (t >= view.a && !out.includes(t)) out.push(t);
    }
    return out;
  }, [view]);

  const cycleLines = useMemo(() => {
    if (!cycle || (view.b - view.a) / cycle.period > 160) return [];
    const out = [];
    const k0 = Math.floor((view.a - cycle.anchor) / cycle.period);
    const k1 = Math.ceil((view.b - cycle.anchor) / cycle.period);
    for (let k = k0; k <= k1; k++) out.push(cycle.anchor + k * cycle.period);
    return out;
  }, [view, cycle]);

  const laneIndex = Object.fromEntries(lanes.map((l, i) => [l.id, i]));
  const height = TOP + lanes.length * LANE_H + 10;

  function down(e) {
    drag.current = { x: e.clientX, a: view.a, b: view.b, moved: false };
    setDragging(true);
  }
  function move(e) {
    const d = drag.current;
    if (!d) return;
    const dx = e.clientX - d.x;
    if (Math.abs(dx) > 3) d.moved = true;
    const dy = (dx / plotW) * (d.b - d.a);
    setView({ a: d.a - dy, b: d.b - dy });
  }
  function up() {
    drag.current = null;
    setDragging(false);
  }

  const zoomTo = (a, b) => setView({ a, b });

  return (
    <>
      <div className="toolbar">
        <span className="sub">
          {fmtYear(view.a)} → {fmtYear(view.b)} · scroll to zoom, drag to pan
        </span>
        <span className="spacer" />
        <button className="btn" onClick={() => zoomTo(-12000, 3200)}>All</button>
        <button className="btn" onClick={() => zoomTo(-4200, 2300)}>Anno Mundi</button>
        <button className="btn" onClick={() => zoomTo(-1300, 2300)}>Axis → now</button>
        <button className="btn" onClick={() => zoomTo(1500, 2250)}>Last 5 cycles</button>
        <button className="btn" onClick={() => zoomTo(nowYear - 150, nowYear + 150)}>Now ±150</button>
      </div>
      <div
        ref={wrap}
        className={'tl-wrap' + (dragging ? ' drag' : '')}
        onPointerDown={down}
        onPointerMove={move}
        onPointerUp={up}
        onPointerLeave={up}
      >
        <svg viewBox={`0 0 ${size.w} ${Math.max(size.h, height)}`} preserveAspectRatio="none">
          {lanes.map((l, i) => (
            <g key={l.id}>
              <rect x={0} y={TOP + i * LANE_H} width={size.w} height={LANE_H} fill={i % 2 ? '#0a0b12' : '#07080d'} />
              <circle cx={14} cy={TOP + i * LANE_H + LANE_H / 2} r={4} fill={l.color} />
              <text className="tl-lane-label" x={26} y={TOP + i * LANE_H + LANE_H / 2 + 4}>{l.label}</text>
            </g>
          ))}
          {ticks.map((t) => (
            <g key={t}>
              <line className="tl-tick" x1={x(t)} x2={x(t)} y1={TOP - 8} y2={height} />
              <text className="tl-tick-label" x={x(t) + 4} y={TOP - 14}>{fmtYear(t)}</text>
            </g>
          ))}
          {cycleLines.map((c) => (
            <line key={'c' + c} x1={x(c)} x2={x(c)} y1={TOP} y2={height} stroke="#d9a94a" strokeOpacity={0.14} strokeDasharray="2 4" />
          ))}
          <line className="tl-now" x1={x(nowYear)} x2={x(nowYear)} y1={TOP - 8} y2={height} />
          <text x={x(nowYear) + 4} y={height - 4} fill="#e2603a" fontSize="11" fontFamily="Consolas, monospace">now</text>
          {items.map((it) => {
            const li = laneIndex[it.lane];
            if (li == null) return null;
            const xa = x(it.year);
            const xb = it.yearEnd != null ? x(it.yearEnd) : xa;
            if (xb < LABEL_W - 20 || xa > size.w + 20) return null;
            const cy = TOP + li * LANE_H + LANE_H / 2;
            const on = picked && picked.id === it.id;
            const pick = (e) => {
              if (drag.current?.moved) return;
              e.stopPropagation();
              onPick(it);
            };
            return (
              <g key={it.id} className="tl-mark" onPointerUp={pick}>
                {xb - xa > 3 ? (
                  <rect x={xa} y={cy - 6} width={xb - xa} height={12} rx={3} fill={it.color} fillOpacity={on ? 0.9 : 0.5} />
                ) : (
                  <circle cx={xa} cy={cy} r={on ? 7 : 5} fill={it.color} stroke={on ? '#fff' : '#07080d'} strokeWidth={1.5} />
                )}
                <title>{`${fmtSpan(it.year, it.yearEnd)} · ${it.title}`}</title>
              </g>
            );
          })}
        </svg>
      </div>
      <div className="detail">
        {picked ? (
          <>
            <h3>{picked.title}</h3>
            <div className="meta">{fmtSpan(picked.year, picked.yearEnd)}{picked.meta ? ' · ' + picked.meta : ''}</div>
            {picked.summary && <p>{picked.summary}</p>}
          </>
        ) : (
          <div className="note">Click a mark for details. Faint gold dashes are Phoenix cycle points; the ember line is now.</div>
        )}
      </div>
    </>
  );
}
