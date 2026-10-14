# يبني خلاصات RSS لكل منصة من posts.json — يقرأها Zapier وينقلها إلى Buffer
import json, datetime
from xml.sax.saxutils import escape
BASE='https://hamedalthiabi-gif.github.io/hamed-media/'
posts=json.load(open('posts.json',encoding='utf-8'))
for plat in ['x','linkedin','tiktok']:
    items=[p for p in posts if p['platform']==plat]
    items.sort(key=lambda p:p['date'],reverse=True)
    out=['<?xml version="1.0" encoding="UTF-8"?>','<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>',
         f'<title>Hamed {plat}</title><link>https://hamedalthiabi.com</link><description>منشورات {plat}</description>']
    for p in items:
        url=BASE+p['media']; typ='video/mp4' if url.endswith('.mp4') else 'image/png'
        dt=datetime.datetime.fromisoformat(p['date']).strftime('%a, %d %b %Y %H:%M:%S +0300')
        out.append(f"<item><title>{escape(p['text'][:80])}</title><description>{escape(p['text'])}</description>"
                   f"<link>{url}</link><guid isPermaLink=\"false\">{p['id']}</guid><pubDate>{dt}</pubDate>"
                   f"<enclosure url=\"{url}\" type=\"{typ}\" length=\"0\"/><media:content url=\"{url}\" type=\"{typ}\"/></item>")
    out.append('</channel></rss>')
    open(f'feeds/{plat}.xml','w',encoding='utf-8').write('\n'.join(out))
print('ok')
