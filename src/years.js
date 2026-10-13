// All years in the app are astronomical: 1 BC = 0, 2 BC = -1. Data files are normalised to this on load.

export function fmtYear(y) {
  if (y == null || Number.isNaN(y)) return '—';
  const r = Math.round(y);
  return r <= 0 ? `${1 - r} BC` : `${r} AD`;
}

export function fmtSpan(a, b) {
  return b == null || b === a ? fmtYear(a) : `${fmtYear(a)} – ${fmtYear(b)}`;
}

// Decimal astronomical year for a JS Date (proleptic Gregorian, good enough for display).
export function decimalYear(d = new Date()) {
  const y = d.getUTCFullYear();
  const start = Date.UTC(y, 0, 1);
  const end = Date.UTC(y + 1, 0, 1);
  return y + (d.getTime() - start) / (end - start);
}

// Position inside a repeating cycle anchored at `anchor` (any cycle point).
export function cyclePos(now, anchor, period) {
  const k = Math.floor((now - anchor) / period);
  const last = anchor + k * period;
  return { index: k, last, next: last + period, frac: (now - last) / period };
}

// Countdown parts from decimal years (365.2425-day years).
export function yearsToParts(years) {
  const totalDays = years * 365.2425;
  const y = Math.floor(totalDays / 365.2425);
  const d = Math.floor(totalDays - y * 365.2425);
  const hFloat = (totalDays - y * 365.2425 - d) * 24;
  const h = Math.floor(hFloat);
  const m = Math.floor((hFloat - h) * 60);
  const s = Math.floor(((hFloat - h) * 60 - m) * 60);
  return { y, d, h, m, s };
}

export function fmtCountdown(years) {
  if (years < 0) return 'passed';
  const { y, d, h, m, s } = yearsToParts(years);
  const pad = (n) => String(n).padStart(2, '0');
  return `${y}y ${d}d ${pad(h)}:${pad(m)}:${pad(s)}`;
}
