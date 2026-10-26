// يحوّل تصميم HTML (agent/designs/*.html) إلى صورة PNG بمقاس 1080×1350
// node agent/tools/render_html.js agent/designs/<file>.html img/<out>.png [width] [height]
const {chromium} = require('playwright'); const path = require('path');
(async () => {
  const [src, out, w = 1080, h = 1350] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({viewport: {width: +w, height: +h}});
  await p.goto('file://' + path.resolve(src)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({path: out}); await b.close();
})();
