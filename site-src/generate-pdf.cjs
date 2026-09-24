// Requires Playwright and an installed Microsoft Edge. Run from the repository root.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  try {
    const page = await browser.newPage();
    await page.goto('file:///' + path.resolve('cv.html').replace(/\\/g, '/'));
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: 'assets/Reyza-Agung-Gunawan-CV.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
