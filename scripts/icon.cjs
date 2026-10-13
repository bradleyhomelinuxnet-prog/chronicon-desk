// Renders build/icon.png (512×512) from an inline SVG: the 138 ring, the Nemesis 60/792 arc, now, and a sun.
// Usage: npx electron scripts/icon.cjs
const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

const S = 512, c = 256, R = 200;
let ticks = '';
for (let i = 0; i < 138; i++) {
  const a = (2 * Math.PI * i) / 138;
  const L = i % 23 === 0 ? 29 : 13;
  const p = (r) => `${(c + r * Math.sin(a)).toFixed(1)},${(c - r * Math.cos(a)).toFixed(1)}`;
  const [x0, y0] = p(R).split(','), [x1, y1] = p(R - L).split(',');
  ticks += `<line x1="${x0}" y1="${y0}" x2="${x1}" y2="${y1}" stroke="${i === 0 ? '#d9a94a' : '#5a6080'}" stroke-width="${i === 0 ? 6 : 2.5}" stroke-linecap="round"/>`;
}
const arc = (r, f) => {
  const a = 2 * Math.PI * f;
  return `M${c},${c - r} A${r},${r} 0 0 1 ${(c + r * Math.sin(a)).toFixed(1)},${(c - r * Math.cos(a)).toFixed(1)}`;
};
const an = (2 * Math.PI * 124) / 138;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${S}" height="${S}" viewBox="0 0 ${S} ${S}">
<circle cx="${c}" cy="${c}" r="244" fill="#07080d" stroke="#23273a" stroke-width="5"/>
${ticks}
<circle cx="${c}" cy="${c}" r="125" fill="none" stroke="#2a2440" stroke-width="18"/>
<path d="${arc(125, 60 / 792)}" fill="none" stroke="#a07ad6" stroke-width="18"/>
<circle cx="${(c + (R - 40) * Math.sin(an)).toFixed(1)}" cy="${(c - (R - 40) * Math.cos(an)).toFixed(1)}" r="17" fill="#e2603a"/>
<circle cx="${c}" cy="${c}" r="55" fill="#d9a94a"/><circle cx="${c}" cy="${c}" r="31" fill="#07080d"/>
</svg>`;

app.whenReady().then(async () => {
  const win = new BrowserWindow({ width: S, height: S, show: false, transparent: true, frame: false, useContentSize: true });
  await win.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(
    `<html><body style="margin:0;background:transparent;overflow:hidden">${svg}</body></html>`));
  await new Promise((r) => setTimeout(r, 400));
  const img = await win.webContents.capturePage({ x: 0, y: 0, width: S, height: S });
  const out = path.join(__dirname, '..', 'build');
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, 'icon.png'), img.resize({ width: S, height: S }).toPNG());
  fs.writeFileSync(path.join(out, 'icon.svg'), svg);
  console.log('build/icon.png');
  app.quit();
});
