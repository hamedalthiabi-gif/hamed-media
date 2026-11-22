# بيانات لوحة «تحليل المحتوى الأسبوعي» (Claude Artifact من نوع Data).
#   python3 agent/dashboard_data.py
# يقرأ agent/engagement/<المنصة>-raw.json وأحدث agent/engagement/weekly/*.md وقسم «التوصيات المعتمدة» في AGENT.md،
# ويكتب agent/engagement/dashboard/posts.json و notes.json (مصفوفة صفوف) لرفعها إلى اللوحة كل أحد.
import json, os, re, glob, datetime
A = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(A, 'engagement'); OUT = os.path.join(E, 'dashboard'); os.makedirs(OUT, exist_ok=True)
NAMES = {'x': 'إكس', 'linkedin': 'لينكدإن', 'tiktok': 'تيك توك'}
LAUNCH = re.compile(r'قـريـبـ|11/11/2026|تنطلق هويتنا|القيم نفسها')


def week_start(d):  # الأسبوع يبدأ الأحد
    return d - datetime.timedelta(days=(d.weekday() + 1) % 7)


posts = []
for p, name in NAMES.items():
    f = os.path.join(E, f'{p}-raw.json')
    if not os.path.exists(f):
        continue
    data = json.load(open(f, encoding='utf-8')); items = data['results'] if isinstance(data, dict) else data
    for i in items:
        s = i.get('statistics')
        if i.get('status') != 'sent' or not s:
            continue
        t = datetime.datetime.fromtimestamp(i['sent_at'], datetime.timezone.utc) + datetime.timedelta(hours=3)
        inter = sum(s.get(k, 0) for k in ('reactions', 'likes', 'comments', 'reposts', 'retweets', 'shares'))
        text = re.sub(r'\{hashtag\|#\|([^}]*)\}', r'#\1', i.get('text', '')).replace('‫', '').replace('‬', '')
        posts.append({'id': str(i.get('id')), 'platform': name, 'date': t.strftime('%Y-%m-%d'), 'time': t.strftime('%H:%M'),
                      'week': week_start(t.date()).isoformat(), 'interactions': inter,
                      'views': s.get('impressions') or s.get('video views') or 0,
                      'rate': s.get('eng. rate', 0), 'launch': bool(LAUNCH.search(text)),
                      'text': ' '.join(text.split())[:110], 'link': i.get('service_link') or ''})
posts.sort(key=lambda r: (r['date'], r['time']))
json.dump(posts, open(os.path.join(OUT, 'posts.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

notes = []
agent = open(os.path.join(A, 'AGENT.md'), encoding='utf-8').read()
m = re.search(r'### التوصيات المعتمدة\n(.*?)(?:\n\n|\n#)', agent, re.S)
for line in (m.group(1).splitlines() if m else []):
    r = re.match(r'- \[(\d{4}-\d\d-\d\d)\] (.*)', line.strip())
    if r:
        notes.append({'kind': 'توصية مطبّقة', 'date': r.group(1), 'text': r.group(2)})
weekly = sorted(glob.glob(os.path.join(E, 'weekly', '*.md')))
if weekly:
    w = open(weekly[-1], encoding='utf-8').read(); d = os.path.basename(weekly[-1])[:-3]
    for head, kind in (('الأعلى والأضعف', 'ملاحظة'), ('سبب ضعف الأسبوع', 'ملاحظة'), ('مقترحات تنتظر الاعتماد', 'مقترح')):
        sec = re.search(r'## ' + head + r'\n(.*?)(?:\n## |\Z)', w, re.S)
        for line in (sec.group(1).splitlines() if sec else []):
            if line.startswith('- '):
                notes.append({'kind': kind, 'date': d, 'text': line[2:].strip()})
json.dump(notes, open(os.path.join(OUT, 'notes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(posts), 'منشورًا،', len(notes), 'ملاحظة')
