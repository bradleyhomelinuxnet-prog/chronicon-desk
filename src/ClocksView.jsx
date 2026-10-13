import { useEffect, useState } from 'react';
import { computeClocks } from './engine.js';

const GROUPS = [
  ['core', 'Chronicon core', 'The cycles the Chronicon is built on'],
  ['maya', 'Maya & moon', 'Long Count, Calendar Round, Metonic gear, lunar phase'],
  ['live', 'Live time', 'The sun over Giza and the civil clocks'],
  ['wall', 'Calendar wall', "Every calendar the engine reads, side by side"],
];

export default function ClocksView({ meta, constants }) {
  const [now, setNow] = useState(() => new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);
  const clocks = computeClocks(now);

  return (
    <div className="view">
      {GROUPS.map(([g, title, blurb]) => (
        <section key={g} style={{ marginBottom: 28 }}>
          <h2 style={{ font: '600 18px var(--serif)', margin: '0 0 2px', color: 'var(--gold)' }}>{title}</h2>
          <div className="note" style={{ marginBottom: 12 }}>{blurb}</div>
          <div className="grid">
            {clocks.filter((c) => c.group === g).map((c) => {
              const m = meta[c.id] || {};
              return (
                <div className="card" key={c.id} style={c.flag ? { borderColor: 'var(--ember)' } : null}>
                  <div className="kicker">{m.name || c.id}</div>
                  <div className="big">{c.value}</div>
                  <div className="sub">{c.sub}</div>
                  {c.bar != null && <div className="bar"><i style={{ width: `${Math.min(Math.max(c.bar, 0), 1) * 100}%` }} /></div>}
                  {m.description && <p>{m.description}</p>}
                  {m.source && <div className="src">{m.source}</div>}
                </div>
              );
            })}
          </div>
        </section>
      ))}
      <section>
        <h2 style={{ font: '600 18px var(--serif)', margin: '0 0 2px', color: 'var(--gold)' }}>Constants</h2>
        <div className="note" style={{ marginBottom: 12 }}>Periods the engine carries with no epoch, so no live position.</div>
        <table>
          <thead><tr><th>Cycle</th><th>Period</th><th>Note</th></tr></thead>
          <tbody>
            {constants.map((c) => (
              <tr key={c.id}>
                <td>{c.name}</td>
                <td className="yr">{c.periodYears != null ? `${c.periodYears} yr` : ''}{c.periodDays != null ? `${c.periodYears != null ? ' · ' : ''}${c.periodDays} d` : ''}</td>
                <td className="tagline">{c.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
