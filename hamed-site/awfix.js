const fs=require('fs');const {JSDOM}=require(require.resolve('jsdom',{paths:['/home/claude/hamed-tools/node_modules']}));
const f=process.argv[2];const dom=new JSDOM(fs.readFileSync(f,'utf8'));const d=dom.window.document;
const fig=[...d.querySelectorAll('.aw-photos figure')].find(x=>x.querySelector('img').getAttribute('src')==='img/n-aw3.webp');if(!fig)throw 'no fig';fig.remove();
const st=[...d.querySelectorAll('style')].pop();st.textContent=st.textContent.replace('.aw-photos{display:grid;grid-template-columns:repeat(3,1fr)','.aw-photos{display:grid;grid-template-columns:repeat(2,1fr);max-width:900px;margin-inline:auto').replace('@media (max-width:820px){.aw-photos{grid-template-columns:1fr 1fr}}','');
fs.writeFileSync(f,'<!doctype html>\n'+d.documentElement.outerHTML);console.log('ok',d.querySelectorAll('.aw-photos figure').length);
