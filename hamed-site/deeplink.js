// رابط مباشر لإصدار: https://hamedalthiabi.com/?utm_...#pubs/pub15 يفتح صفحة الإصدارات ثم قارئ الإصدار نفسه.
// usage: node deeplink.js file.html  (idempotent)
const fs = require('fs'); const f = process.argv[2]; let s = fs.readFileSync(f, 'utf8');
if (s.includes('id="pub-deeplink"')) { console.log('deeplink: already present'); process.exit(0); }
const a = "function route(){const h=location.hash.slice(1);";
if (!s.includes(a)) throw new Error('route() not found');
s = s.replace(a, "function route(){const h=location.hash.slice(1).split('/')[0];");
const js = `<script id="pub-deeplink">(function(){
  function go(){var m=location.hash.match(/^#pubs\\/(pub\\d+)$/);if(!m)return;
    var b=document.querySelector('.read-pub[data-pdf="pubs/'+m[1]+'.pdf"]');if(!b)return;
    b.scrollIntoView({block:'center'});if(window.pdfjsLib)b.click();}
  window.addEventListener('hashchange',function(){setTimeout(go,0)});
  if(document.readyState==='complete')go();else window.addEventListener('load',go,{once:true});
})();</script>`;
s = s.replace(/<\/body>(?![\s\S]*<\/body>)/, js + '</body>');
fs.writeFileSync(f, s); console.log('deeplink: added');
