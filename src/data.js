// Merges the extracted data into one model. Everything inside the app is an astronomical year (1 BC = 0).
// clocks.json is already astronomical; phoenix.json stores N BC as -N (no year zero), so it is shifted here.
import clocksRaw from './data/clocks.json';
import phoenixRaw from './data/phoenix.json';
import { MAY_NODES, nemesisWindows } from './engine.js';

const fromHistorical = (y) => (y == null ? null : y < 0 ? y + 1 : y);

export const LANES = [
  { id: 'phoenix', label: 'Phoenix 138', color: '#d9a94a' },
  { id: 'nemesis', label: 'Nemesis X 792', color: '#a07ad6' },
  { id: 'nibiru', label: 'Nibiru', color: '#d46a8c' },
  { id: 'ledger', label: 'Chronicon ledger', color: '#5fa8d3' },
  { id: 'events', label: 'Events', color: '#e2603a' },
  { id: 'witnesses', label: 'Witnesses', color: '#4fb38a' },
  { id: 'maya', label: 'Maya baktuns', color: '#3fa7a0' },
];
const COLOR = Object.fromEntries(LANES.map((l) => [l.id, l.color]));

export const clockMeta = Object.fromEntries(clocksRaw.clocks.map((c) => [c.id, c]));
export const constantClocks = clocksRaw.clocks.filter((c) =>
  ['saros', 'inex', 'precession', 'jupiter-saturn', 'jupiter-return', 'saturn-return', 'uranus-return', 'chiron-return', 'year-lengths', 'solar-year-length'].includes(c.id),
);

export const phoenixDates = [...phoenixRaw.phoenixDates, ...phoenixRaw.projections]
  .map((p) => ({ ...p, year: fromHistorical(p.year) }))
  .sort((a, b) => a.year - b.year);

export const events = phoenixRaw.events
  .map((e, i) => ({ ...e, id: 'ev' + i, year: fromHistorical(e.year), yearEnd: fromHistorical(e.yearEnd) }))
  .sort((a, b) => a.year - b.year);

export const witnesses = phoenixRaw.witnesses.map((w, i) => ({ ...w, id: 'w' + i, year: fromHistorical(w.year) }));

export const ledger = clocksRaw.calendricDates.map((c, i) => ({ ...c, id: 'cd' + i }));

// Nibiru is not defined in the Chronicon engine files. The user's Chronotecture-Charts redesign names it
// at 1254 (entering) and 1314 (exiting) — the same years as the Nemesis X inner window. Shown as charted.
const NIBIRU = {
  id: 'nibiru',
  name: 'Nibiru',
  aliases: ['Anunnaki planet'],
  periodYears: null,
  lastPassages: [
    { year: 1254, note: 'Anunnaki planet Nibiru passes over ecliptic, entering' },
    { year: 1314, note: 'Nibiru seen from Earth as it exits the system' },
  ],
  nextPassages: [],
  description:
    'Named only in the Chronotecture-Charts redesign. Its 1254 entry and 1314 exit fall on the Nemesis X inner window (1254–1314); the charts do not say whether the two are one body.',
  source: 'Chronotecture-Charts/redesign/vid.html:111-112 · redesign/iic.html:131',
};

export const bodies = [...clocksRaw.bodies.filter((b) => b.id !== 'nibiru'), NIBIRU];

export const openQuestions = [
  ...clocksRaw.openQuestions.map((q) => ({ from: 'Clocks & calendrics', q })),
  ...phoenixRaw.openQuestions.map((q) => ({ from: 'Phoenix & films', q })),
  {
    from: 'Chronicon Desk',
    q: 'Phoenix numbering: the films count Phoenix N = AM/138 from Year One (2040 = Phoenix 43); the engine lattice counts nodes from 4309 BC (2040 = node 47). The app shows the films’ number with the lattice node beside it.',
  },
  { from: 'Chronicon Desk', q: '2040 date: engine countdown 15 May, site countdown 16 May, film transcript 17 May. The live clock follows the engine (15 May).' },
];

export const cycle = { period: 138, anchor: -3894 }; // Year One (3895 BC), AM 0 in the engine's arithmetic

export function phoenixNumber(astro) {
  return (astro + 3894) / 138;
}

// ── Timeline items ───────────────────────────────────────────────
export function timelineItems() {
  const items = [];
  phoenixDates.forEach((p, i) =>
    items.push({ id: 'ph' + i, lane: 'phoenix', year: p.year, title: p.label, summary: p.note || '', meta: p.source, color: COLOR.phoenix }),
  );
  nemesisWindows(-6000, 3000).forEach(([a, b], i) =>
    items.push({ id: 'nw' + i, lane: 'nemesis', year: a, yearEnd: b, title: 'Nemesis X inside Sol (60-year window)', summary: 'Enters when mod(year − 462, 792) = 0; 60 years inside, 732 outside.', meta: 'engine NEM_ENTER {mod:462, step:792}', color: COLOR.nemesis }),
  );
  bodies.forEach((b) =>
    [...b.lastPassages, ...b.nextPassages].forEach((p, i) => {
      const lane = b.id === 'nibiru' ? 'nibiru' : b.id === 'phoenix' ? null : 'nemesis';
      if (!lane) return;
      items.push({ id: `bp-${b.id}-${i}`, lane, year: p.year, title: `${b.name}: ${p.note}`, summary: b.description, meta: b.source, color: COLOR[lane] });
    }),
  );
  ledger.forEach((c) =>
    items.push({ id: c.id, lane: 'ledger', year: c.year, title: c.title, summary: c.note, meta: c.source, color: COLOR.ledger }),
  );
  events.forEach((e) =>
    items.push({ id: e.id, lane: 'events', year: e.year, yearEnd: e.yearEnd, title: e.title, summary: e.summary, meta: (e.tags || []).join(' · '), color: COLOR.events }),
  );
  witnesses.filter((w) => w.year != null).forEach((w) =>
    items.push({ id: w.id, lane: 'witnesses', year: w.year, title: w.name, summary: w.testimony, meta: w.era, color: COLOR.witnesses }),
  );
  MAY_NODES.slice(0, -1).forEach((y, i) =>
    items.push({ id: 'bk' + i, lane: 'maya', year: y, yearEnd: MAY_NODES[i + 1], title: `Baktun ${i + 1}/13`, summary: `${MAY_NODES[i + 1] - y}-year span in the engine's hard-coded node list.`, meta: 'MAY_NODES', color: i % 2 ? '#2d7f7a' : COLOR.maya }),
  );
  return items;
}
