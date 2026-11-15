# يجلب المنشورات المرسلة لكل قناة من Buffer API مباشرة (بديل Zapier) لتحليل التفاعل الأسبوعي.
# يعمل على GitHub Actions (.github/workflows/engagement-fetch.yml) بالمفتاح المحفوظ في السر BUFFER_API_KEY.
#   python3 agent/buffer_sent.py
# الناتج:
#   agent/engagement/buffer-schema.json   حقول المنشور المتاحة في الواجهة (للتشخيص)
#   agent/engagement/api/<المنصة>.json     الاستجابة كما هي
#   agent/engagement/<المنصة>-raw.json     بصيغة engagement.py، ويُكتب فقط إن وُجدت أرقام التفاعل
import json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer_publish import gql, s, ORG, FALLBACK

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engagement')
API = os.path.join(D, 'api')
STAT = re.compile(r'stat|metric|insight|analytic|engag', re.I)
TYPE_Q = '{ name kind fields { name args { name } type { name kind ofType { name kind ofType { name kind ofType { name kind } } } } } }'


def tname(t):  # اسم النوع الأساسي ونوعه بعد فك NON_NULL وLIST
    while t.get('ofType'):
        t = t['ofType']
    return t['name'], t['kind']


def describe(name):
    return gql('query { __type(name: %s) %s }' % (s(name), TYPE_Q))['__type']


def selection(name, depth=0):
    """حقول عددية/نصية للنوع، مع نزول مستوى واحد في الأنواع الكائنية."""
    t = describe(name)
    parts = []
    for f in t.get('fields') or []:
        if f.get('args'):
            continue
        n, k = tname(f['type'])
        if k in ('SCALAR', 'ENUM'):
            parts.append(f['name'])
        elif k == 'OBJECT' and depth < 2:
            sub = selection(n, depth + 1)
            if sub:
                parts.append('%s { %s }' % (f['name'], sub))
    return ' '.join(parts)


def flat(v, out, prefix=''):  # تحويل أي بنية إحصاءات إلى {اسم: رقم}
    if isinstance(v, dict):
        if 'name' in v and 'value' in v and isinstance(v['value'], (int, float)):
            out[str(v['name']).lower()] = v['value']
            return out
        for k, x in v.items():
            flat(x, out, k)
    elif isinstance(v, list):
        for x in v:
            flat(x, out, prefix)
    elif isinstance(v, (int, float)) and not isinstance(v, bool) and prefix:
        out[prefix.lower()] = v
    return out


def main():
    os.makedirs(API, exist_ok=True)
    post = describe('Post')
    fields = []
    for f in post['fields']:
        if f.get('args'):
            continue
        n, k = tname(f['type'])
        fields.append({'name': f['name'], 'type': n, 'kind': k})
    stat_fields = [f for f in fields if STAT.search(f['name']) or STAT.search(f['type'] or '')]
    json.dump({'Post': fields, 'stat_fields': stat_fields}, open(os.path.join(D, 'buffer-schema.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('حقول الإحصاءات المتاحة:', [f['name'] for f in stat_fields] or 'لا شيء')

    base = [f['name'] for f in fields if f['kind'] in ('SCALAR', 'ENUM')]
    extra = []
    for f in stat_fields:
        if f['kind'] in ('SCALAR', 'ENUM'):
            continue
        sub = selection(f['type'])
        if sub:
            extra.append('%s { %s }' % (f['name'], sub))
    sel = ' '.join(base + extra)
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=45)).strftime('%Y-%m-%dT%H:%M:%SZ')
    found_stats = False
    for plat, cid in FALLBACK.items():
        nodes, after = [], None
        for _ in range(10):
            q = ('query { posts(first: 100%s, input: { organizationId: %s, filter: { status: [sent], channelIds: [%s], '
                 'dueAt: { start: %s } } }) { edges { node { %s } } pageInfo { hasNextPage endCursor } } }'
                 % (', after: %s' % s(after) if after else '', s(ORG), s(cid), s(since), sel))
            res = gql(q)['posts']
            nodes += [e['node'] for e in res['edges']]
            if not res['pageInfo']['hasNextPage']:
                break
            after = res['pageInfo']['endCursor']
        json.dump(nodes, open(os.path.join(API, plat + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        results = []
        for n in nodes:
            st = {}
            for f in stat_fields:
                flat(n.get(f['name']), st, f['name'])
            when = n.get('sentAt') or n.get('dueAt')
            if not st or not when:
                continue
            ts = datetime.datetime.fromisoformat(when.replace('Z', '+00:00')).timestamp()
            results.append({'id': n.get('id'), 'status': 'sent', 'sent_at': int(ts), 'text': n.get('text', ''),
                            'type': n.get('type'), 'service_link': n.get('externalLink'), 'statistics': st})
        print(f'{plat}: {len(nodes)} منشور مرسل، منها {len(results)} بأرقام تفاعل')
        if results:
            found_stats = True
            json.dump({'results': results, 'source': 'buffer-api'},
                      open(os.path.join(D, plat + '-raw.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    if not found_stats:
        print('لم تُرجع الواجهة أرقام تفاعل؛ لم تُستبدل ملفات raw.')


if __name__ == '__main__':
    main()
