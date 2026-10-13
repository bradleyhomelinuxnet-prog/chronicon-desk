import { useEffect, useMemo, useState } from 'react';
import Timeline from './Timeline.jsx';
import ClocksView from './ClocksView.jsx';
import { WheelView, EventsView, WitnessesView, BodiesView, NotesView } from './Views.jsx';
import { LANES, timelineItems, clockMeta, constantClocks, events, witnesses, bodies, openQuestions, cycle, phoenixNumber } from './data.js';
import { phoenix, nemesis, PHOENIX_2040 } from './engine.js';
import { decimalYear, fmtCountdown } from './years.js';

const TABS = [
  ['clocks', 'Clocks'],
  ['timeline', 'Timeline'],
  ['wheel', '138 Wheel'],
  ['events', 'Events', events.length],
  ['witnesses', 'Witnesses', witnesses.length],
  ['bodies', 'Nemesis X · Nibiru', bodies.length],
  ['notes', 'Source notes', openQuestions.length],
];

export default function App() {
  const [tab, setTab] = useState('clocks');
  const [now, setNow] = useState(() => new Date());
  const [picked, setPicked] = useState(null);
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const items = useMemo(() => timelineItems(), []);
  const nowYear = decimalYear(now);
  const yr = now.getUTCFullYear();
  const ph = phoenix(yr);
  const nx = nemesis(yr);

  return (
    <div className="app">
      <header className="top">
        <div className="brand">
          Chronicon Desk
          <small>Phoenix 138 · Nemesis X 792 · every clock</small>
        </div>
        <div className="now">
          <div><span>Anno Mundi</span><b>{(yr + 3894).toLocaleString()}</b></div>
          <div><span>Phoenix {Math.floor(phoenixNumber(ph.next))} · 2040</span><b>{fmtCountdown((PHOENIX_2040 - now.getTime()) / 3.15576e10)}</b></div>
          <div><span>Nemesis X</span><b>{nx.inner ? 'inside' : `${nx.enterNext - yr} yr out`}</b></div>
          <div><span>UTC</span><b>{now.toISOString().slice(11, 19)}</b></div>
        </div>
      </header>
      <nav className="tabs" role="tablist">
        {TABS.map(([id, label, count]) => (
          <button key={id} role="tab" aria-selected={tab === id} onClick={() => setTab(id)}>
            {label}{count != null && <span className="count">{count}</span>}
          </button>
        ))}
      </nav>
      {tab === 'clocks' && <ClocksView meta={clockMeta} constants={constantClocks} />}
      {tab === 'timeline' && (
        <div className="view flush">
          <Timeline items={items} lanes={LANES} nowYear={nowYear} cycle={cycle} picked={picked} onPick={setPicked} />
        </div>
      )}
      {tab === 'wheel' && <WheelView nowYear={nowYear} />}
      {tab === 'events' && <EventsView />}
      {tab === 'witnesses' && <WitnessesView />}
      {tab === 'bodies' && <BodiesView nowYear={nowYear} />}
      {tab === 'notes' && <NotesView />}
    </div>
  );
}
