// Live clock engine — a port of the clock math in Chronicon_Engine_v2.html.
// Years are astronomical (1 BC = 0). Each clock returns { id, group, value, sub, bar?, flag? }.
import { fmtYear, decimalYear, fmtCountdown } from './years.js';

export const mod = (n, m) => ((n % m) + m) % m;

export const PHX = { mod: 108, step: 138, base: -4308 };
export const NEM = { mod: 462, step: 792, inside: 60 };
export const NER = { mod: 162, step: 600, base: -5238 };
export const MAY_NODES = [-3112, -2712, -2312, -1912, -1512, -1112, -712, -318, 76, 470, 864, 1258, 1652, 2046];
export const PHOENIX_2040 = Date.UTC(2040, 4, 15, 0, 0, 0);

// Proleptic Gregorian Julian Day Number from astronomical year.
export function jdn(y, m, d) {
  const a = Math.floor((14 - m) / 12);
  const yy = y + 4800 - a;
  const mm = m + 12 * a - 3;
  return d + Math.floor((153 * mm + 2) / 5) + 365 * yy + Math.floor(yy / 4) - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
}

export function phoenix(astro) {
  const prev = astro - mod(astro - PHX.mod, PHX.step);
  return { prev, next: prev + PHX.step, into: astro - prev, idx: Math.round((prev - PHX.base) / PHX.step) + 1 };
}

export function nemesis(astro) {
  const offset = mod(astro - NEM.mod, NEM.step);
  const enterPrev = astro - offset;
  const inner = offset < NEM.inside;
  return { offset, inner, enterPrev, exit: enterPrev + NEM.inside, enterNext: enterPrev + NEM.step };
}

export function ner(astro) {
  const off = mod(astro - NER.mod, NER.step);
  const start = astro - off;
  return { off, start, next: start + NER.step, num: Math.floor((astro - NER.base) / NER.step) + 1, decan: Math.floor(off / 60) + 1 };
}

export function baktun(astro) {
  if (astro < MAY_NODES[0]) return { label: 'PRE-COUNT', start: null, end: MAY_NODES[0] };
  if (astro >= MAY_NODES[MAY_NODES.length - 1]) return { label: '13.0.0.0.0 complete', start: MAY_NODES[13], end: null };
  let bi = 0;
  while (!(MAY_NODES[bi] <= astro && astro < MAY_NODES[bi + 1])) bi++;
  return { label: `BAKTUN ${bi + 1}/13`, n: bi + 1, start: MAY_NODES[bi], end: MAY_NODES[bi + 1] };
}

const SYN = 29.530588853;
const NEWMOON_J2000 = 2451550.1;
const PHASES = ['New', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 'Full', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'];
const TZ = ['Imix', "Ik'", "Ak'b'al", "K'an", 'Chikchan', 'Kimi', "Manik'", 'Lamat', 'Muluk', 'Ok', 'Chuwen', 'Eb', "B'en", 'Ix', 'Men', "K'ib'", "Kab'an", "Etz'nab'", 'Kawak', 'Ajaw'];
const HAAB = ['Pop', "Wo'", 'Sip', "Sotz'", 'Sek', 'Xul', "Yaxk'in", 'Mol', "Ch'en", 'Yax', "Sak'", 'Keh', 'Mak', "K'ank'in", 'Muwan', 'Pax', "K'ayab", "Kumk'u"];
const STEM = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'];
const BRANCH = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai'];
const ELEM = ['Wood', 'Wood', 'Fire', 'Fire', 'Earth', 'Earth', 'Metal', 'Metal', 'Water', 'Water'];
const ANIMAL = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig'];
const EGY = ['Thoth', 'Phaophi', 'Athyr', 'Choiak', 'Tybi', 'Mechir', 'Phamenoth', 'Pharmouthi', 'Pachons', 'Payni', 'Epiphi', 'Mesore'];
const FR = ['Vendémiaire', 'Brumaire', 'Frimaire', 'Nivôse', 'Pluviôse', 'Ventôse', 'Germinal', 'Floréal', 'Prairial', 'Messidor', 'Thermidor', 'Fructidor'];

const pad = (n) => String(n).padStart(2, '0');
const hms = (h) => {
  const t = mod(h, 24);
  const H = Math.floor(t);
  const M = Math.floor((t - H) * 60);
  const S = Math.floor(((t - H) * 60 - M) * 60);
  return `${pad(H)}:${pad(M)}:${pad(S)}`;
};
const n = (x) => x.toLocaleString('en-US');

function intlYear(date, calendar) {
  try {
    const s = new Intl.DateTimeFormat(`en-US-u-ca-${calendar}`, { year: 'numeric', month: 'long', day: 'numeric' }).format(date);
    return s;
  } catch {
    return '—';
  }
}

export function computeClocks(now = new Date()) {
  const astro = now.getUTCFullYear();
  const m = now.getUTCMonth() + 1;
  const d = now.getUTCDate();
  const J = jdn(astro, m, d);
  const dy = decimalYear(now);
  const out = [];
  const add = (c) => out.push(c);

  // ── Archaix core ────────────────────────────────────────────────
  const p = phoenix(astro);
  // Phoenix N = AM/138 counted from Year One (the films' numbering); the lattice node index runs from 4309 BC.
  const pn = (y) => (y + 3894) / 138;
  add({ id: 'phoenix-138', group: 'core', value: `Phoenix ${pn(p.prev)} · ${p.into}/138`,
    sub: `Phoenix ${pn(p.prev)} ${fmtYear(p.prev)} · Phoenix ${pn(p.next)} ${fmtYear(p.next)} (${p.next - astro} yr) · lattice node ${p.idx}`, bar: p.into / 138 });

  const ms = PHOENIX_2040 - now.getTime();
  const days = Math.floor(ms / 86400000);
  add({ id: 'phoenix-countdown', group: 'core', value: ms > 0 ? fmtCountdown(ms / 3.15576e10) : 'ARRIVED',
    sub: `${n(days)} days to 15 May 2040` + (days % 138 === 0 ? ' · ×138 today' : '') + (days % 19 === 0 ? ' · ×19 today' : ''),
    flag: days % 138 === 0 || days % 19 === 0 });

  const nx = nemesis(astro);
  add({ id: 'nemesis-x-792', group: 'core',
    value: nx.inner ? `INSIDE · year ${nx.offset + 1}/60` : `OUTSIDE · ${nx.enterNext - astro} yr to return`,
    sub: nx.inner ? `entered ${fmtYear(nx.enterPrev)} · exits ${fmtYear(nx.exit)}` : `last window ${fmtYear(nx.enterPrev)}–${fmtYear(nx.exit)} · returns ${fmtYear(nx.enterNext)}`,
    bar: nx.inner ? nx.offset / 60 : (astro - nx.exit) / 732 });

  const nr = ner(astro);
  add({ id: 'ner-600', group: 'core', value: `NER ${nr.num} · decan ${nr.decan}/10`,
    sub: `began ${fmtYear(nr.start)} · next ${fmtYear(nr.next)}`, bar: nr.off / 600 });

  add({ id: 'annus-mundi', group: 'core', value: `AM ${n(astro + 3894)}`, sub: 'Year One = 3895 BC · AD = AM − 3894' });
  add({ id: 'cataclysm-era', group: 'core', value: `${n(astro + 5238)} yr`, sub: 'since the Nemesis Cataclysm, 5239 BC' });

  const turns = J - jdn(-3894, 1, 1);
  add({ id: 'anunna-turnings', group: 'core', value: `${n(turns)} šar`,
    sub: `${(turns / 360).toFixed(1)} Draconian yr · ${(turns / 216000).toFixed(3)} NER · ${(turns / 144000).toFixed(3)} baktun` });

  // ── Maya and moon ──────────────────────────────────────────────
  const b = baktun(astro);
  const lc = astro + 3112;
  add({ id: 'mayan-long-count', group: 'maya', value: b.label,
    sub: `LC year ${n(lc)}` + (b.end != null ? ` · 13.0.0.0.0 in ${fmtYear(2046)} (${2046 - astro} yr)` : '') + (String(lc).includes('138') ? ' · 138 sigil' : ''),
    bar: b.start != null && b.end != null ? (astro - b.start) / (b.end - b.start) : null });

  const ld = J - 584283;
  const hp = mod(ld + 348, 365);
  const haab = hp < 360 ? `${mod(hp, 20)} ${HAAB[Math.floor(hp / 20)]}` : `${hp - 360} Wayeb`;
  add({ id: 'mayan-calendar-round', group: 'maya', value: `${mod(ld + 3, 13) + 1} ${TZ[mod(ld + 19, 20)]} · ${haab}`, sub: 'Tzolkin · Haab — 52-year round' });

  const age = mod(J + (now.getUTCHours() / 24 - 0.5) - NEWMOON_J2000, SYN);
  const frac = age / SYN;
  const illum = (1 - Math.cos(2 * Math.PI * frac)) / 2;
  add({ id: 'lunar-synodic', group: 'maya', value: PHASES[Math.floor(mod(frac + 1 / 16, 1) * 8) % 8],
    sub: `age ${age.toFixed(1)} d · ${(illum * 100).toFixed(0)}% lit · lunation ${Math.floor((J - 2423436.40347) / SYN) + 1}`, bar: frac });

  const metYr = mod(astro - 2026, 19) + 1;
  add({ id: 'metonic-19', group: 'maya', value: `year ${metYr}/19`, sub: '235 lunations = 19 years · reference 2026', bar: (metYr - 1) / 19 });

  // ── Live time ──────────────────────────────────────────────────
  const utcH = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
  const doy = Math.floor((Date.UTC(astro, m - 1, d) - Date.UTC(astro, 0, 0)) / 86400000);
  const B = (2 * Math.PI * (doy - 81)) / 364;
  const eot = 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B);
  add({ id: 'giza-apparent-solar', group: 'live', value: hms(utcH + 31.1342 / 15 + eot / 60), sub: `equation of time ${eot >= 0 ? '+' : ''}${eot.toFixed(1)} min · 31.13° E` });
  let cairo = '—';
  try {
    cairo = new Intl.DateTimeFormat('en-GB', { timeZone: 'Africa/Cairo', hour: '2-digit', minute: '2-digit', second: '2-digit', timeZoneName: 'shortOffset' }).format(now);
  } catch { /* zone data missing */ }
  add({ id: 'cairo-civil', group: 'live', value: cairo.split(' ')[0], sub: cairo.split(' ').slice(1).join(' ') || 'Africa/Cairo' });
  add({ id: 'utc', group: 'live', value: hms(utcH), sub: now.toISOString().slice(0, 10) });
  add({ id: 'local-meridian', group: 'live', value: hms(now.getHours() + now.getMinutes() / 60 + now.getSeconds() / 3600), sub: Intl.DateTimeFormat().resolvedOptions().timeZone });

  // ── Calendar wall ──────────────────────────────────────────────
  add({ id: 'hebrew-anno-mundi', group: 'wall', value: intlYear(now, 'hebrew'), sub: `Archaix AM ${n(astro + 3894)} vs Hebrew AM` });
  add({ id: 'coptic', group: 'wall', value: intlYear(now, 'coptic'), sub: 'Year of the Martyrs, from 284' });
  const ed = J - 1448638;
  const edoy = mod(ed, 365);
  add({ id: 'egyptian-civil-nabonassar', group: 'wall', value: `Year ${n(Math.floor(ed / 365) + 1)}`,
    sub: edoy < 360 ? `${mod(edoy, 30) + 1} ${EGY[Math.floor(edoy / 30)]}` : `epagomenal day ${edoy - 359}` });
  add({ id: 'sothic', group: 'wall', value: `${mod(astro - 139, 1460)}/1460`, sub: 'since the 139 AD Sothic rising', bar: mod(astro - 139, 1460) / 1460 });
  add({ id: 'islamic-hijri', group: 'wall', value: intlYear(now, 'islamic'), sub: 'from 622' });
  add({ id: 'persian-solar-hijri', group: 'wall', value: intlYear(now, 'persian'), sub: 'from 622' });
  add({ id: 'indian-saka', group: 'wall', value: intlYear(now, 'indian'), sub: 'from 78' });
  add({ id: 'ethiopic', group: 'wall', value: intlYear(now, 'ethiopic'), sub: 'Amete Mihret' });
  const ci = mod(astro - 4, 60);
  add({ id: 'chinese-sexagenary', group: 'wall', value: `${STEM[ci % 10]}-${BRANCH[ci % 12]}`, sub: `${ELEM[ci % 10]} ${ANIMAL[ci % 12]} · year ${ci + 1}/60 (from Chinese New Year)` });
  add({ id: 'byzantine-world-era', group: 'wall', value: `AM ${n(m >= 9 ? astro + 5509 : astro + 5508)}`, sub: 'from 1 Sep 5509 BC' });
  add({ id: 'kali-yuga', group: 'wall', value: n(astro + 3101), sub: 'from 3102 BC' });
  add({ id: 'buddhist-era', group: 'wall', value: `BE ${n(astro + 543)}`, sub: 'astro + 543' });
  add({ id: 'holocene', group: 'wall', value: `${n(astro + 10000)} HE`, sub: 'astro + 10000' });
  const fJD = J - 2375839;
  if (fJD >= 1) {
    const fy = Math.floor((fJD - 1) / 365.2422) + 1;
    const fdoy = Math.floor(fJD - 1 - (fy - 1) * 365.2422);
    add({ id: 'french-republican', group: 'wall', value: `An ${fy}`, sub: fdoy < 360 ? `${mod(fdoy, 30) + 1} ${FR[Math.floor(fdoy / 30)]} (approx.)` : 'Sansculottides' });
  }
  add({ id: 'julian-day', group: 'wall', value: `JDN ${n(J)}`, sub: String(J) === String(J).split('').reverse().join('') ? 'palindromic day' : 'days since 4713 BC (Julian)' });
  add({ id: 'unix', group: 'wall', value: n(Math.round(now.getTime() / 1000)), sub: 'seconds since 1970' });
  add({ id: 'year-progress', group: 'wall', value: `${((dy - astro) * 100).toFixed(4)}%`, sub: `of ${astro} elapsed`, bar: dy - astro });

  return out;
}

// For the timeline: Phoenix nodes and Nemesis windows across a range.
export function phoenixNodes(a, b) {
  const out = [];
  for (let y = PHX.base; y <= b; y += PHX.step) if (y >= a) out.push(y);
  return out;
}
export function nemesisWindows(a, b) {
  const out = [];
  const k0 = Math.floor((a - NEM.mod) / NEM.step);
  for (let k = k0; NEM.mod + k * NEM.step <= b; k++) {
    const s = NEM.mod + k * NEM.step;
    if (s >= -5238) out.push([s, s + NEM.inside]);
  }
  return out;
}
