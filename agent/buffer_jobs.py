# مهام Buffer لمرة واحدة من agent/buffer_jobs.json: حذف منشور مجدول، أو حفظ منشور من queue.json مسودةً في Buffer.
# يعمل على GitHub Actions (.github/workflows/buffer-jobs.yml) بالسر BUFFER_API_KEY. المنفّذ يُنقل إلى "done".
#   {"todo": [{"draft": "<id في queue.json>"}, {"delete": "<Buffer post id>"}], "done": [...]}
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buffer_publish as B

JOBS = os.path.join(B.ROOT, 'agent', 'buffer_jobs.json')


def draft(pid, ch):
    p = next(x for x in json.load(open(B.QUEUE, encoding='utf-8')) if x['id'] == pid)
    fields = ['text: %s' % B.s(p['text']), 'channelId: %s' % B.s(ch[p['platform']]),
              'schedulingType: automatic', 'mode: addToQueue', 'saveToDraft: true']
    if p.get('media'):
        fields.append(B.asset(p['media']))
    r = B.gql(('mutation { createPost(input: { %s }) { ... on PostActionSuccess { post { id } } '
               '... on MutationError { message } } }') % ', '.join(fields))['createPost']
    if not r.get('post'):
        raise RuntimeError(r.get('message'))
    return r['post']['id']


def delete(bid):
    r = B.gql('mutation { deletePost(input: { id: %s }) { __typename ... on MutationError { message } } }' % B.s(bid))
    r = r['deletePost']
    if r.get('message'):
        raise RuntimeError(r['message'])
    return r['__typename']


def main():
    jobs = json.load(open(JOBS, encoding='utf-8'))
    _, ch = B.channels()
    left, failed = [], 0
    for j in jobs.get('todo', []):
        try:
            res = draft(j['draft'], ch) if 'draft' in j else delete(j['delete'])
            j['result'] = res
            j['at'] = datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z'
            jobs.setdefault('done', []).append(j)
            print('✓', j)
        except Exception as e:
            failed += 1
            j['error'] = str(e)[:300]
            left.append(j)
            print('✗', j)
    jobs['todo'] = left
    json.dump(jobs, open(JOBS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if failed:
        sys.exit(f'فشلت {failed} مهمة.')


if __name__ == '__main__':
    main()
