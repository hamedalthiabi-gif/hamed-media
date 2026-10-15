# ينقل منشورات اليوم من agent/queue.json إلى posts.json ثم يبني خلاصات RSS
import json, datetime, subprocess, sys, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
today=(sys.argv[1] if len(sys.argv)>1 else (datetime.datetime.utcnow()+datetime.timedelta(hours=3)).date().isoformat())
q=json.load(open('agent/queue.json',encoding='utf-8'))
posts=json.load(open('posts.json',encoding='utf-8'))
ids={p['id'] for p in posts}
new=[dict(p,date=today+'T'+p.get('time','06:00')+':00') for p in q if p['date']==today and p['id'] not in ids]
posts+=new
json.dump(posts,open('posts.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
subprocess.run([sys.executable,'build_feeds.py'],check=True)
print(f'{today}: أُضيف {len(new)} منشور')
for p in new: print('-',p['platform'],p['id'])
