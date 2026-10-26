# تحليل التفاعل وأفضل أوقات النشر من منشورات Buffer المرسلة.
# المصدر: إجراء Zapier «Buffer → New Sent Item» (buffer_new_sent_item) لكل قناة، تُحفظ نتيجته كما هي في
#   agent/engagement/<المنصة>-raw.json   (المنصة: x أو linkedin أو tiktok)
# ثم: python3 agent/engagement.py  → يكتب agent/engagement/summary.json ويطبع متوسط التفاعل لكل فترة نشر.
# مقياس الترتيب: إكس = الوصول (reach) + ١٠×(إعجاب+إعادة نشر)، لينكدإن وتيك توك = التعليقات والإعجابات المتاحة.
import json, os, datetime, statistics, glob
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engagement')
SLOTS = [(5, 8, 'فجر/مبكر ٥–٨ص'), (8, 11, 'صباح ٨–١١ص'), (11, 14, 'ظهر ١١ص–٢م'), (14, 18, 'عصر ٢–٦م'),
         (18, 21, 'مساء ٦–٩م'), (21, 24, 'ليل ٩–١٢م'), (0, 5, 'بعد منتصف الليل')]


def score(platform, s):
    if platform == 'x':
        return s.get('reach', 0) + 10 * (s.get('likes', 0) + s.get('retweets', 0))
    return sum(v for v in s.values() if isinstance(v, (int, float)))


def slot(h):
    return next(n for a, b, n in SLOTS if a <= h < b)


out = {}
for f in sorted(glob.glob(os.path.join(D, '*-raw.json'))):
    plat = os.path.basename(f).split('-')[0]
    data = json.load(open(f, encoding='utf-8')); items = data['results'] if isinstance(data, dict) else data
    by = {}
    for p in items:
        if p.get('status') != 'sent' or 'statistics' not in p:
            continue
        t = datetime.datetime.fromtimestamp(p['sent_at'], datetime.timezone.utc) + datetime.timedelta(hours=3)
        if datetime.datetime.now(datetime.timezone.utc) - t.replace(tzinfo=datetime.timezone.utc) < datetime.timedelta(hours=27):
            continue  # منشور حديث لم يكتمل تفاعله
        by.setdefault(slot(t.hour), []).append({'at': t.strftime('%Y-%m-%d %H:%M'), 'score': score(plat, p['statistics']),
                                               'stats': p['statistics'], 'type': p.get('type'), 'text': p.get('text', '')[:60]})
    out[plat] = {k: {'posts': len(v), 'avg': round(statistics.mean(x['score'] for x in v)),
                     'median': round(statistics.median(x['score'] for x in v)), 'items': v} for k, v in by.items()}
    print(f'== {plat}')
    for k, v in sorted(out[plat].items(), key=lambda kv: -kv[1]['median']):
        print(f"  {k}: {v['posts']} منشور، الوسيط {v['median']}، المتوسط {v['avg']}")
out['updated'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open(os.path.join(D, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
