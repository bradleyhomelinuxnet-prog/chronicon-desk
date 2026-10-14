// Dev helper: screenshot one page.
// Usage: SNAP_URL=<http-url-or-file> SNAP_OUT=<out.png> [SNAP_W=1500 SNAP_H=1400] npx electron scripts/snap.cjs
const { app, BrowserWindow } = require('electron');
const fs = require('fs');

const url = process.env.SNAP_URL;
const out = process.env.SNAP_OUT;
const w = +(process.env.SNAP_W || 1500);
const h = +(process.env.SNAP_H || 1400);

app.whenReady().then(async () => {
  const win = new BrowserWindow({ width: w, height: h, show: false, backgroundColor: '#0b0f1a' });
  await (/^https?:\/\//.test(url) ? win.loadURL(url) : win.loadFile(url));
  await new Promise((r) => setTimeout(r, 2500));
  fs.writeFileSync(out, (await win.webContents.capturePage()).toPNG());
  console.log(out);
  app.quit();
});
