# ينقل منشورات اليوم التي حان وقتها من agent/queue.json إلى posts.json ثم يبني خلاصات RSS
# يُشغَّل قبل كل موعد نشر بنحو ١٠ دقائق (٨:٥٠ص و١٠:٥٠ص و٨:٥٠م بتوقيت الرياض)، فيصل المنشور إلى Buffer في موعده.
# python3 agent/publish_today.py            → اليوم، حتى الوقت الحالي + ١٥ دقيقة
# python3 agent/publish_today.py 2026-10-18 → كل منشورات ذلك اليوم (للاختبار اليدوي)
import json, datetime, subprocess, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
now = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
if len(sys.argv) > 1: today, limit = sys.argv[1], '23:59'
else: today, limit = now.date().isoformat(), (now + datetime.timedelta(minutes=15)).strftime('%H:%M')
q = json.load(open('agent/queue.json', encoding='utf-8'))
posts = json.load(open('posts.json', encoding='utf-8'))
ids = {p['id'] for p in posts}
new = [dict(p, date=today + 'T' + p.get('time', '09:00') + ':00') for p in q
       if p['date'] == today and p['id'] not in ids and p.get('time', '09:00') <= limit]
posts += new
json.dump(posts, open('posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, 'build_feeds.py'], check=True)
print(f'{today} حتى {limit}: أُضيف {len(new)} منشور')
for p in new: print('-', p['platform'], p['id'])
