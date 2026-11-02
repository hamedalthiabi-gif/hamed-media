const fs=require('fs');const {JSDOM}=require(require.resolve('jsdom',{paths:['/home/claude/hamed-tools/node_modules']}));
const f=process.argv[2];const dom=new JSDOM(fs.readFileSync(f,'utf8'));const d=dom.window.document;
const ul=d.querySelector('.awards .aw-list');
const after=[...ul.children].find(li=>li.textContent.includes('جائزة العمل التطوعي'));if(!after)throw 'x';
after.insertAdjacentHTML('afterend','<li><b>تطوع احترافي</b><span>المركز الوطني لتنمية القطاع غير الربحي</span></li>');
ul.insertAdjacentHTML('beforeend','<li><b>هاكثون التنمية الاجتماعية الأول</b><span>المركز الثاني، مشروع «تعزيز»</span></li>');
fs.writeFileSync(f,'<!doctype html>\n'+d.documentElement.outerHTML);console.log([...ul.children].map(l=>l.querySelector('b').textContent).join(' | '));
