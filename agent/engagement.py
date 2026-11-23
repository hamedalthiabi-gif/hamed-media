# تحليل التفاعل وأفضل أوقات النشر من منشورات Buffer المرسلة.
# المصدر: إجراء Zapier «Buffer → New Sent Item» (buffer_new_sent_item) لكل قناة، تُحفظ نتيجته كما هي في
#   agent/engagement/<المنصة>-raw.json   (المنصة: x أو linkedin أو tiktok)
# ثم: python3 agent/engagement.py  → يكتب agent/engagement/summary.json ويطبع متوسط التفاعل لكل فترة نشر.
# مقياس الترتيب: مجموع التفاعل (تفاعلات + تعليقات + إعادة نشر + مشاركات)، لا المشاهدات.
import json, os, datetime, statistics, glob
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engagement')
SLOTS = [(5, 8, 'فجر/مبكر ٥–٨ص'), (8, 11, 'صباح ٨–١١ص'), (11, 14, 'ظهر ١١ص–٢م'), (14, 18, 'عصر ٢–٦م'),
         (18, 21, 'مساء ٦–٩م'), (21, 24, 'ليل ٩–١٢م'), (0, 5, 'بعد منتصف الليل')]


def score(platform, s):
    # التفاعل = إعجابات/تفاعلات + تعليقات + إعادة نشر + مشاركات (صيغة Buffer API الحالية، مع الحقول القديمة)
    keys = ('reactions', 'likes', 'comments', 'reposts', 'retweets', 'shares')
    return sum(s.get(k, 0) for k in keys if isinstance(s.get(k, 0), (int, float)))


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

# أفضل وقت لكل منصة ولكل يوم من أيام الأسبوع (بطلب تغريد ٢٣ نوفمبر: الأوقات تتبع أفضل التفاعل، لا وقتًا ثابتًا كل يوم).
# القاعدة: الساعة ذات أعلى وسيط تفاعل بين الساعات التي فيها ٣ منشورات على الأقل. لليوم المعيّن تُعتمد ساعته الخاصة إن كان
# فيها ٣ منشورات على الأقل في ذلك اليوم وتفوقت على الساعة العامة للمنصة بـ٣٠٪ فأكثر، وإلا فالساعة العامة.
# والساعة العامة لا تتغير عن الحالية (DEFAULT) إلا بالشرط نفسه.
# «explore»: ثاني أفضل ساعة، يُجرَّب فيها منشور واحد أسبوعيًا لكل منصة لتكوين بيانات مقارنة.
# الناتج agent/engagement/best_times.json، ويقرؤه الروتين اليومي لحقل time في queue.json.
DAYS = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
MIN = {'linkedin': ':00', 'x': ':30', 'tiktok': ':00'}
DEFAULT = {'linkedin': 9, 'x': 9, 'tiktok': 21}
EXPLORE = {'linkedin': '13:00', 'x': '12:30', 'tiktok': '19:00'}  # إن لم توجد ساعة ثانية فيها ٣ منشورات
BT = os.path.join(D, 'best_times.json')
if os.path.exists(BT):  # الوقت الحالي = آخر وقت معتمد
    for k, v in json.load(open(BT, encoding='utf-8')).items():
        if isinstance(v, dict) and v.get('default'):
            DEFAULT[k] = int(v['default'][:2])
best = {}
for plat, slots in out.items():
    if plat == 'updated':
        continue
    items = [it for v in slots.values() for it in v['items']]
    byh, bydh = {}, {}
    for it in items:
        t = datetime.datetime.strptime(it['at'], '%Y-%m-%d %H:%M')
        byh.setdefault(t.hour, []).append(it['score'])
        bydh.setdefault((DAYS[t.weekday()], t.hour), []).append(it['score'])
    ranked = sorted(((statistics.median(v), h, len(v)) for h, v in byh.items() if len(v) >= 3), reverse=True)
    cur = DEFAULT.get(plat, 9)
    cm = statistics.median(byh[cur]) if byh.get(cur) else 0
    # لا يُستبدل الوقت الحالي إلا بساعة فيها ٣ منشورات على الأقل وتتفوق عليه بـ٣٠٪ فأكثر
    gh, gm = (ranked[0][1], ranked[0][0]) if ranked and ranked[0][0] >= cm * 1.3 else (cur, cm)
    m = MIN.get(plat, ':00')
    days = {}
    for d in DAYS:
        cand = sorted(((statistics.median(v), h, len(v)) for (dd, h), v in bydh.items() if dd == d and len(v) >= 3), reverse=True)
        h = cand[0][1] if cand and cand[0][0] >= gm * 1.3 and cand[0][1] != gh else gh
        days[d] = f'{h:02d}{m}'
    best[plat] = {'default': f'{gh:02d}{m}', 'days': days,
                  'explore': next((f'{h:02d}{m}' for _, h, _ in ranked if h != gh), EXPLORE.get(plat)),
                  'evidence': [{'hour': h, 'posts': n, 'median': md} for md, h, n in ranked]}
best['updated'] = out['updated']
json.dump(best, open(BT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('== أفضل الأوقات:', {p: v['default'] for p, v in best.items() if p != 'updated'})
