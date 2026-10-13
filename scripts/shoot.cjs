// Dev helper: open the built app off-screen, click through every tab and save a PNG of each.
// Usage: npx electron scripts/shoot.cjs <outDir>
const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

const out = process.argv[process.argv.length - 1];
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

app.whenReady().then(async () => {
  fs.mkdirSync(out, { recursive: true });
  const win = new BrowserWindow({ width: 1440, height: 900, show: false, backgroundColor: '#07080d' });
  await win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  await wait(800);
  const errors = [];
  win.webContents.on('console-message', (e) => { if (e.level === 'error') errors.push(e.message); });
  const tabs = await win.webContents.executeJavaScript(`[...document.querySelectorAll('[role=tab]')].map(b => b.textContent)`);
  for (let i = 0; i < tabs.length; i++) {
    await win.webContents.executeJavaScript(`document.querySelectorAll('[role=tab]')[${i}].click()`);
    await wait(600);
    const img = await win.webContents.capturePage();
    const file = path.join(out, `${String(i + 1).padStart(2, '0')}-${tabs[i].replace(/[^a-z0-9]+/gi, '-').toLowerCase()}.png`);
    fs.writeFileSync(file, img.toPNG());
    console.log(file);
  }
  if (errors.length) console.log('CONSOLE ERRORS:\n' + errors.join('\n'));
  app.quit();
});
