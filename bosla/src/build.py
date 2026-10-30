import sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
out_dir = pathlib.Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
here = pathlib.Path(__file__).parent

def rep(s, old, new):
    if old not in s:
        raise SystemExit("missing: " + old[:80])
    return s.replace(old, new, 1)

p = src
p = rep(p, 'const next={points:(cur.points||0)+n,awarded:{...(cur.awarded||{}),[key]:true}};',
           'const next={points:(cur.points||0)+n,awarded:{...(cur.awarded||{}),[key]:true},name:((R.prefs.profile||{}).name||"")};')
p = rep(p, 'if(!R.uid)return `<h2>${t("acT")}</h2><p class="lead">${t("acLogin")}</p>`;',
           'if(!R.uid)return `<h2>${t("acT")}</h2><p class="lead">${t("acLogin")}</p>${window.BOSLA_AUTH?window.BOSLA_AUTH.form(S.lang):""}`;')
p = rep(p, 'return `<h2>${t("acT")}</h2><div class="kpi" id="acKpi">',
           'return `<div class="cmhead"><h2>${t("acT")}</h2>${window.BOSLA_AUTH?window.BOSLA_AUTH.logout(S.lang):""}</div><div class="kpi" id="acKpi">')

head = '''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="بوصلة: المرجع التعليمي للعاملين في القطاع غير الربحي">
<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
<script src="config.js"></script>
<script>
''' + (here / "shim.js").read_text() + '''
</script>
</head><body>
'''
(out_dir / "index.html").write_text(head + p + "\n</body></html>\n")
cfg = out_dir / "config.js"
if not cfg.exists():
    cfg.write_text('// Supabase project settings (public values). Leave empty to run the site in read-only mode.\nwindow.BOSLA_CONFIG = { url: "", anonKey: "" };\n')
pass
print("built", out_dir / "index.html")
