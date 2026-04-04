const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://localhost:8080/');
  await page.waitForLoadState('networkidle');

  console.log('Test 1 - No JS errors:', errors.length === 0 ? 'PASS' : 'FAIL: ' + errors.join('; '));

  const notesType = await page.evaluate(() => typeof userNotes);
  console.log('Test 2 - userNotes is object:', notesType === 'object' ? 'PASS' : 'FAIL');

  await page.click('#readingMode');
  await page.waitForTimeout(300);
  const studyBtn = await page.$('button.rw-study-btn');
  if (!studyBtn) { console.log('Test 3 - study btn: FAIL'); await browser.close(); process.exit(0); }
  await studyBtn.click();
  await page.waitForTimeout(300);

  const card = await page.$('#studyCard');
  await card.click();
  await page.waitForTimeout(200);

  const textarea = await page.$('#mnNoteInput');
  console.log('Test 3 - Note textarea on mnemonic phase:', textarea ? 'PASS' : 'FAIL');

  if (textarea) {
    await textarea.fill('looks like a snake saying ahh');
    await page.waitForTimeout(400);
    const saved = await page.$eval('#mnNoteSaved', el => el.textContent);
    console.log('Test 4 - Saved indicator:', saved.includes('Saved') ? 'PASS' : 'FAIL:' + saved);

    await card.click();
    await page.waitForTimeout(200);
    const backVisible = await page.$eval('#cardBackNote', el => el.style.display !== 'none');
    const backText = await page.$eval('#cardBackNote', el => el.innerText);
    console.log('Test 5 - Note on back phase:', backVisible && backText.includes('snake') ? 'PASS' : 'FAIL:' + backText);

    const noteVal = await page.evaluate(() => userNotes);
    const charNote = Object.values(noteVal)[0];
    console.log('Test 6 - userNotes global:', charNote && charNote.includes('snake') ? 'PASS' : 'FAIL:' + JSON.stringify(noteVal));
  }

  console.log('JS errors during test:', errors.length ? errors.join('; ') : 'none');
  await browser.close();
})();
