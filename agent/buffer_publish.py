# يجدول منشورات اليوم والغد من agent/queue.json في Buffer مباشرة (Buffer API).
# يعمل على GitHub Actions (.github/workflows/buffer.yml) ويقرأ المفتاح من السر BUFFER_API_KEY فقط،
# فلا يظهر المفتاح في أي ملف أو سجل.
#   python3 agent/buffer_publish.py          → جدولة ما لم يُجدول بعد
#   python3 agent/buffer_publish.py check    → اختبار المفتاح وعرض القنوات فقط (لا ينشر شيئًا)
import json, os, sys, datetime, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
QUEUE = os.path.join(ROOT, 'agent', 'queue.json')
DONE = os.path.join(ROOT, 'agent', 'buffer_scheduled.json')
ORG = '6a4bdb54a23c84347c8879d3'
SERVICE = {'linkedin': 'linkedin', 'x': 'twitter', 'tiktok': 'tiktok'}
FALLBACK = {'linkedin': '6a4bdb7040483446287754cf', 'x': '6a4bdb9c4048344628775568',
            'tiktok': '6a4bdc5f404834462877580e'}
REPO = os.environ.get('GITHUB_REPOSITORY', 'hamedalthiabi-gif/hamed-media')
REF = os.environ.get('GITHUB_SHA', 'main')


def gql(query):
    key = os.environ.get('BUFFER_API_KEY', '').strip()
    if not key:
        sys.exit('BUFFER_API_KEY غير موجود في أسرار المستودع؛ لم يُنشر شيء.')
    req = urllib.request.Request('https://api.buffer.com', data=json.dumps({'query': query}).encode(),
                                 headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)
    if res.get('errors'):
        raise RuntimeError(json.dumps(res['errors'], ensure_ascii=False))
    return res['data']


def s(v):  # نص GraphQL آمن
    return json.dumps(v, ensure_ascii=False)


def channels():
    data = gql('query { channels(input: { organizationId: %s }) { id name service } }' % s(ORG))
    found = {c['service']: c['id'] for c in data['channels']}
    return data['channels'], {p: found.get(svc, FALLBACK[p]) for p, svc in SERVICE.items()}


def asset(media):
    url = f'https://raw.githubusercontent.com/{REPO}/{REF}/{media}'
    if media.lower().endswith('.mp4'):
        return 'assets: [{ video: { url: %s } }]' % s(url)
    return 'assets: [{ image: { url: %s } }]' % s(url)


def main():
    if not os.environ.get('BUFFER_API_KEY', '').strip():
        print('لم يُضف السر BUFFER_API_KEY بعد؛ لم يُنشر شيء.')
        sys.exit(1 if sys.argv[1:] == ['check'] else 0)
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        lst, _ = channels()
        for c in lst:
            print('-', c['service'], c['name'], c['id'])
        print('المفتاح يعمل.')
        return
    now = datetime.datetime.now(datetime.timezone.utc)
    riyadh = now + datetime.timedelta(hours=3)
    days = {riyadh.date().isoformat(), (riyadh.date() + datetime.timedelta(days=1)).isoformat()}
    queue = json.load(open(QUEUE, encoding='utf-8'))
    done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}
    todo = [p for p in queue if p.get('date') in days and p.get('platform') in SERVICE and p['id'] not in done
            and p.get('status') != 'draft']  # المسودة لا تُجدول حتى تعتمدها تغريد
    if not todo:
        print('لا منشورات جديدة للجدولة.')
        return
    _, ch = channels()
    failed = 0
    for p in sorted(todo, key=lambda p: (p['date'], p.get('time', '09:00'))):
        local = datetime.datetime.fromisoformat(f"{p['date']}T{p.get('time', '09:00')}:00")
        due = local - datetime.timedelta(hours=3)
        due = due.replace(tzinfo=datetime.timezone.utc)
        due = max(due, now + datetime.timedelta(minutes=3))  # إن فات الموعد يُنشر بعد دقائق
        fields = ['text: %s' % s(p['text']), 'channelId: %s' % s(ch[p['platform']]),
                  'schedulingType: automatic', 'mode: customScheduled',
                  'dueAt: %s' % s(due.strftime('%Y-%m-%dT%H:%M:%S.000Z'))]
        if p.get('media'):
            fields.append(asset(p['media']))
        q = ('mutation { createPost(input: { %s }) { ... on PostActionSuccess { post { id dueAt } } '
             '... on MutationError { message } } }') % ', '.join(fields)
        try:
            r = gql(q)['createPost']
        except Exception as e:
            r = {'message': str(e)}
        if r.get('post'):
            done[p['id']] = r['post']['id']
            print(f"✓ {p['platform']} {p['date']} {p.get('time')} → {r['post']['id']}")
            json.dump(done, open(DONE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        else:
            failed += 1
            print(f"✗ {p['platform']} {p['id']}: {r.get('message')}")
    if failed:
        sys.exit(f'فشل {failed} منشور.')


if __name__ == '__main__':
    main()
