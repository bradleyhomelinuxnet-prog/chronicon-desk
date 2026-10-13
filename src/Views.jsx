import { useMemo, useState } from 'react';
import { fmtYear, fmtSpan } from './years.js';
import { mod, phoenix, nemesis } from './engine.js';
import { events, witnesses, bodies, openQuestions, phoenixDates, ledger, cycle, phoenixNumber } from './data.js';

const match = (q, ...fields) => !q || fields.some((f) => f && String(f).toLowerCase().includes(q.toLowerCase()));

// ── Cycle wheel ──────────────────────────────────────────────────
// Every dated item folded onto the 138-year ring by its phase from Year One; the inner ring does the same on 792.
export function WheelView({ nowYear }) {
  const [hover, setHover] = useState(null);
  const R = 250, C = 300;
  const pt = (frac, r) => [C + r * Math.sin(2 * Math.PI * frac), C - r * Math.cos(2 * Math.PI * frac)];

  const dots = useMemo(() => {
    // Items sharing a phase stack inward so a crowded Phoenix year reads as a column, not one dot;
    // spacing tightens so even the busiest phase stays outside the Nemesis ring.
    const all = [
      ...phoenixDates.map((p) => ({ y: p.year, t: p.label, c: '#d9a94a' })),
      ...events.map((e) => ({ y: e.year, t: e.title, c: '#e2603a' })),
      ...ledger.map((l) => ({ y: l.year, t: l.title, c: '#5fa8d3' })),
    ];
    const count = {};
    all.forEach((d) => { const ph = mod(d.y - cycle.anchor, 138); count[ph] = (count[ph] || 0) + 1; });
    const seen = {};
    return all.map((d) => {
      const ph = mod(d.y - cycle.anchor, 138);
      const k = (seen[ph] = (seen[ph] || 0) + 1) - 1;
      return { ...d, r: R - 4 - k * Math.min(8.5, 100 / count[ph]) };
    });
  }, []);

  const pNow = mod(nowYear - cycle.anchor, 138) / 138;
  const nx = nemesis(Math.floor(nowYear));
  const nNow = mod(nowYear - 462, 792) / 792;
  const ph = phoenix(Math.floor(nowYear));
  const onNode = dots.filter((d) => mod(d.y - cycle.anchor, 138) === 0).length;

  return (
    <div className="view">
      <div className="wheel-layout">
        <div className="wheel">
          <svg viewBox="0 0 600 600">
            <circle cx={C} cy={C} r={R + 14} fill="none" stroke="#23273a" />
            <circle cx={C} cy={C} r={R - 50} fill="none" stroke="#23273a" />
            <circle cx={C} cy={C} r={130} fill="none" stroke="#2a2440" strokeWidth={10} />
            {/* Nemesis inner 60-year arc on the 792 ring */}
            <path d={(() => { const [x0, y0] = pt(0, 130); const [x1, y1] = pt(60 / 792, 130); return `M${x0},${y0} A130,130 0 0 1 ${x1},${y1}`; })()} stroke="#a07ad6" strokeWidth={10} fill="none" />
            {Array.from({ length: 138 }, (_, i) => {
              const [x0, y0] = pt(i / 138, R + 14);
              const [x1, y1] = pt(i / 138, R + (i % 19 === 0 ? 24 : 18));
              return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke={i === 0 ? '#d9a94a' : '#3a3f57'} strokeWidth={i === 0 ? 3 : 1} />;
            })}
            {[0, 23, 46, 69, 92, 115].map((i) => {
              const [x, y] = pt(i / 138, R + 40);
              return <text key={i} x={x} y={y} fill="#8d8a80" fontSize="12" textAnchor="middle" dominantBaseline="middle">{i}</text>;
            })}
            {dots.map((d, i) => {
              const [x, y] = pt(mod(d.y - cycle.anchor, 138) / 138, d.r);
              return (
                <circle key={i} cx={x} cy={y} r={hover === i ? 6 : 3.5} fill={d.c} fillOpacity={0.85}
                  onMouseEnter={() => setHover(i)} onMouseLeave={() => setHover(null)} style={{ cursor: 'pointer' }} />
              );
            })}
            {(() => { const [x, y] = pt(pNow, R + 14); return <circle cx={x} cy={y} r={8} fill="none" stroke="#e2603a" strokeWidth={2.5} />; })()}
            {(() => { const [x, y] = pt(nNow, 130); return <circle cx={x} cy={y} r={7} fill="#e2603a" />; })()}
            <text x={C} y={C - 22} fill="#d9a94a" fontSize="30" textAnchor="middle" fontFamily="Georgia, serif">{Math.floor(nowYear) - ph.prev}/138</text>
            <text x={C} y={C + 6} fill="#8d8a80" fontSize="12" textAnchor="middle">years into the cycle</text>
            <text x={C} y={C + 30} fill="#a07ad6" fontSize="12" textAnchor="middle">Nemesis X {nx.inner ? 'inside' : 'outside'} · {mod(Math.floor(nowYear) - 462, 792)}/792</text>
          </svg>
        </div>
        <div>
          <h2 style={{ font: '600 20px var(--serif)', color: 'var(--gold)', margin: '0 0 8px' }}>The 138 ring</h2>
          <p className="note" style={{ fontSize: 13 }}>
            Every dated item is folded onto one 138-year turn, measured from Year One (3895 BC). Items at the top tick land on a
            Phoenix year; clusters elsewhere show recurring offsets. Gold = Phoenix dates, ember = events, blue = Chronicon ledger.
            The violet inner ring is the 792-year Nemesis X orbit, with its 60-year inner window highlighted; the ember dot is now.
          </p>
          <div className="card" style={{ marginTop: 14 }}>
            {hover != null ? (
              <>
                <div className="kicker">{fmtYear(dots[hover].y)} · phase {mod(dots[hover].y - cycle.anchor, 138)}/138</div>
                <h3 style={{ marginTop: 4 }}>{dots[hover].t}</h3>
              </>
            ) : (
              <>
                <div className="kicker">Now</div>
                <h3 style={{ marginTop: 4 }}>Phoenix {Math.floor(phoenixNumber(ph.next))} due {fmtYear(ph.next)}</h3>
                <div className="sub">last: Phoenix {Math.floor(phoenixNumber(ph.prev))} in {fmtYear(ph.prev)} · lattice node {ph.idx}</div>
                <div className="sub" style={{ marginTop: 6 }}>{onNode} of {dots.length} dated items sit exactly on a Phoenix year</div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Events ───────────────────────────────────────────────────────
export function EventsView() {
  const [q, setQ] = useState('');
  const [tag, setTag] = useState(null);
  const tags = useMemo(() => {
    const c = {};
    events.forEach((e) => (e.tags || []).forEach((t) => (c[t] = (c[t] || 0) + 1)));
    return Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 24);
  }, []);
  const rows = events.filter((e) => (!tag || (e.tags || []).includes(tag)) && match(q, e.title, e.summary));
  return (
    <div className="view flush" style={{ gridTemplateRows: 'auto 1fr' }}>
      <div className="toolbar">
        <input type="search" placeholder="Search events…" value={q} onChange={(e) => setQ(e.target.value)} />
        <div className="chips" style={{ marginTop: 0 }}>
          {tags.map(([t, n]) => (
            <button key={t} className={'chip' + (tag === t ? ' on' : '')} onClick={() => setTag(tag === t ? null : t)}>{t} {n}</button>
          ))}
        </div>
      </div>
      <div style={{ overflow: 'auto', padding: '0 22px 30px' }}>
        <table>
          <thead><tr><th>Year</th><th>AM</th><th>Phase</th><th>Event</th></tr></thead>
          <tbody>
            {rows.map((e) => (
              <tr key={e.id}>
                <td className="yr">{fmtSpan(e.year, e.yearEnd)}</td>
                <td className="yr" style={{ color: 'var(--muted)' }}>{e.year + 3894}</td>
                <td className="yr" style={{ color: mod(e.year - cycle.anchor, 138) === 0 ? 'var(--gold)' : 'var(--muted)' }}>{mod(e.year - cycle.anchor, 138)}/138</td>
                <td>
                  <b>{e.title}</b>
                  <div>{e.summary}</div>
                  <div className="tagline">{(e.tags || []).join(' · ')} — {e.source}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!rows.length && <div className="empty">No events match.</div>}
      </div>
    </div>
  );
}

// ── Witnesses ────────────────────────────────────────────────────
export function WitnessesView() {
  const [q, setQ] = useState('');
  const rows = witnesses
    .filter((w) => match(q, w.name, w.era, w.testimony))
    .sort((a, b) => (a.year ?? 1e9) - (b.year ?? 1e9));
  return (
    <div className="view flush" style={{ gridTemplateRows: 'auto 1fr' }}>
      <div className="toolbar">
        <input type="search" placeholder="Search witnesses…" value={q} onChange={(e) => setQ(e.target.value)} />
        <span className="sub">{rows.length} witnesses</span>
      </div>
      <div style={{ overflow: 'auto', padding: '16px 22px 30px' }}>
        <div className="grid">
          {rows.map((w) => (
            <div className="card" key={w.id}>
              <div className="kicker">{w.year != null ? fmtYear(w.year) + ' · ' : ''}{w.era}</div>
              <h3 style={{ marginTop: 4 }}>{w.name}</h3>
              <p>{w.testimony}</p>
              {w.eventRefs?.length > 0 && <div className="chips">{w.eventRefs.map((r) => <span key={r} className="chip">{r}</span>)}</div>}
              <div className="src">{w.source}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ── Bodies ───────────────────────────────────────────────────────
export function BodiesView({ nowYear }) {
  return (
    <div className="view">
      <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))' }}>
        {bodies.map((b) => {
          const next = [...b.nextPassages].map((p) => p.year).filter((y) => y >= nowYear).sort((x, y) => x - y)[0];
          return (
            <div className="card" key={b.id}>
              <div className="kicker">{b.periodYears ? `${b.periodYears}-year period` : 'no stated period'}{b.aliases?.length ? ' · ' + b.aliases.join(', ') : ''}</div>
              <h3 style={{ marginTop: 4, fontSize: 20 }}>{b.name}</h3>
              {next != null && <div className="big" style={{ color: 'var(--ember)' }}>next {fmtYear(next)} · {Math.round(next - nowYear)} yr</div>}
              <p>{b.description}</p>
              <table style={{ marginTop: 10 }}>
                <tbody>
                  {[...b.lastPassages.map((p) => ({ ...p, k: 'past' })), ...b.nextPassages.map((p) => ({ ...p, k: 'next' }))].map((p, i) => (
                    <tr key={i}>
                      <td className="yr" style={{ color: p.k === 'next' ? 'var(--ember)' : undefined }}>{fmtYear(p.year)}</td>
                      <td style={{ fontSize: 13 }}>{p.note}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="src">{b.source}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── Source notes ─────────────────────────────────────────────────
export function NotesView() {
  return (
    <div className="view">
      <h2 style={{ font: '600 20px var(--serif)', color: 'var(--gold)', margin: '0 0 4px' }}>Source notes</h2>
      <p className="note" style={{ marginBottom: 16 }}>
        Where the source files disagree with each other, or where the app had to choose. Nothing here is corrected silently: the
        data is shown as the files give it, and these are the places to rule on.
      </p>
      <table>
        <thead><tr><th style={{ width: 170 }}>Area</th><th>Note</th></tr></thead>
        <tbody>
          {openQuestions.map((o, i) => (
            <tr key={i}><td className="tagline">{o.from}</td><td>{o.q}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
