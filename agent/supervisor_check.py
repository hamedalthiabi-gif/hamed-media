#!/usr/bin/env python3
"""فحص آلي لملفات وكلاء حامد في المستودع. يطبع تقريرًا JSON بالمشكلات.
الاستخدام: python3 agent/supervisor_check.py [YYYY-MM-DD]
لا يعدّل أي ملف."""
import json, os, re, sys, datetime as dt
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, *p)
riyadh = dt.timezone(dt.timedelta(hours=3))
today = sys.argv[1] if len(sys.argv) > 1 else dt.datetime.now(riyadh).date().isoformat()
now = dt.datetime.now(riyadh)

issues = []
def add(sev, agent, code, msg, ref=""):
    if f"{code}:{ref}" in globals().get("ack", {}):
        return
    issues.append({"severity": sev, "agent": agent, "code": code, "msg": msg, "ref": ref})

def load(p, default):
    try:
        with open(A(p), encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        add("high", "content-daily", "bad-json", f"ملف غير صالح: {p} ({e})", p)
        return default

def norm(t):
    t = re.sub(r"https?://\S+", "", t or "")
    return re.sub(r"\s+", " ", t).strip()[:60]

queue = load("agent/queue.json", [])
sched = load("agent/buffer_scheduled.json", {})
# ما راجعه المشرف سابقًا وثبت أنه ليس خطأ: {"<code>:<ref>": "السبب"}
ack = load("agent/supervisor/ack.json", {})
window = (dt.date.fromisoformat(today) - dt.timedelta(days=3)).isoformat()

# ١) تكرار المعرّفات والنصوص (الأهم: منع النشر المكرر)
ids = defaultdict(int)
texts = defaultdict(list)
for p in queue:
    ids[p.get("id")] += 1
    texts[(p.get("platform"), norm(p.get("text")))].append(p.get("id"))
for i, n in ids.items():
    if n > 1:
        add("high", "content-daily", "dup-id", f"المعرّف مكرر {n} مرات في queue.json", i)
for (plat, t), lst in texts.items():
    if t and len(lst) > 1:
        add("high", "content-daily", "dup-text", f"نص متطابق لأكثر من منشور على {plat}", ", ".join(lst))

# ٢) قواعد المحتوى
tiktok_media = defaultdict(list)
for p in queue:
    pid, plat, txt = p.get("id"), p.get("platform"), p.get("text") or ""
    d, media = p.get("date", ""), p.get("media") or ""
    medias = media if isinstance(media, list) else ([media] if media else [])
    media = medias[0] if medias else ""
    if "أ. حامد الذيابي" in txt or "أ.حامد الذيابي" in txt:
        add("mid", "content-daily", "name-in-text", "ذكر «أ. حامد الذيابي» في نص المنشور (ممنوع)", pid)
    if re.search(r"(^|\n)\s*المصدر\s*:", txt):
        add("mid", "content-daily", "source-line", "سطر «المصدر:» في النص (ممنوع)", pid)
    if "استدامة العطاء" in txt and re.search(r"وأثر(?!ٌ)\s+يمتد", txt):
        add("low", "content-daily", "slogan", "الشعار يُكتب «وأثرٌ يمتد» بالتنوين", pid)
    if not p.get("source") and not p.get("campaign"):
        add("low", "content-daily", "no-source", "منشور بلا حقل source", pid)
    if plat == "tiktok":
        if media and not media.lower().endswith(".mp4"):
            add("high", "content-daily", "tiktok-not-video", "تيك توك بوسائط ليست فيديو (المسموح فيديو حقيقي أو مقطع بودكاست فقط)", pid)
        if media:
            tiktok_media[media].append(pid)
    if plat == "x":
        l = len(re.sub(r"https?://\S+", "x" * 23, txt))
        if l > 280:
            add("mid", "content-daily", "x-too-long", f"تغريدة طولها {l} حرفًا (الحد ٢٨٠)", pid)
    if d >= "2026-11-11" and p.get("identity") not in (None, "new"):
        add("mid", "content-daily", "old-identity", "هوية قديمة بعد إطلاق الهوية الجديدة", pid)
    for m in medias:
        if not m.startswith("http") and not os.path.exists(A(m)):
            add("high", "content-daily", "media-missing", f"ملف الوسائط غير موجود: {m}", pid)
    # المواعيد
    is_draft = p.get("status") == "draft"
    in_buffer = pid in sched
    try:
        when = dt.datetime.fromisoformat(f"{d}T{p.get('time','00:00')}:00+03:00")
    except ValueError:
        add("mid", "content-daily", "bad-date", "تاريخ أو وقت غير صالح", pid); continue
    recent = d >= window
    if recent and not is_draft and not in_buffer and when < now:
        add("high", "buffer", "missed", f"فات موعده ({d} {p.get('time')}) ولم يُسجَّل في Buffer", pid)
    if recent and is_draft and when < now:
        add("mid", "content-daily", "stale-draft", f"مسودة فات موعدها ({d} {p.get('time')}) دون اعتماد", pid)
    elif is_draft and d == today:
        add("low", "content-daily", "draft-today", "مسودة اليوم تنتظر اعتماد تغريد", pid)
for m, lst in tiktok_media.items():
    if len(lst) > 1:
        add("high", "content-daily", "tiktok-reused", f"الفيديو نفسه في أكثر من منشور تيك توك: {m}", ", ".join(lst))

# ٣) سجل Buffer: معرّفات لا وجود لها في الطابور
qids = set(ids)
orphan = [k for k in sched if k not in qids]
if orphan:
    add("low", "buffer", "orphan-log", f"{len(orphan)} معرّفًا في buffer_scheduled.json غير موجود في queue.json", ", ".join(orphan[:5]))

# ٤) مخرجات الوكلاء الدورية
last_sun = (dt.date.fromisoformat(today) - dt.timedelta(days=(dt.date.fromisoformat(today).isoweekday() % 7)))
wk = A("agent", "engagement", "weekly", f"{last_sun.isoformat()}.md")
if not os.path.exists(wk):
    add("mid", "content-analysis", "no-weekly-report", f"لا يوجد تقرير التحليل الأسبوعي لـ {last_sun.isoformat()}", "agent/engagement/weekly/")
if not os.path.exists(A("agent", "content_analysis.py")):
    add("low", "content-analysis", "missing-script", "ملف agent/content_analysis.py غير موجود ووكيل التحليل يطلبه", "agent/content_analysis.py")

pc = load("agent/podcast_clips.json", None)
if pc is None:
    add("low", "podcast-clips", "no-log", "سجل المقاطع agent/podcast_clips.json غير موجود", "")
failed = A("podcast", "failed.txt")
if os.path.exists(failed) and open(failed, encoding="utf-8").read().strip():
    add("mid", "podcast-fetch", "fetch-failed", "حلقات فشل جلبها في podcast/failed.txt", "podcast/failed.txt")

sev_order = {"high": 0, "mid": 1, "low": 2}
issues.sort(key=lambda x: sev_order[x["severity"]])
print(json.dumps({"date": today, "queue_size": len(queue), "issues": issues}, ensure_ascii=False, indent=2))
