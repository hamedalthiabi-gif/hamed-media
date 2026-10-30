const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
const svg=fs.readFileSync(process.argv[2],'utf8');const out=process.argv[3];
for(const [n,s] of [['icon-192.png',192],['icon-512.png',512],['apple-touch-icon.png',180],['favicon-32.png',32]]){
 await p.setViewportSize({width:s,height:s});await p.setContent(`<html><body style="margin:0">${svg.replace('<svg ','<svg width="'+s+'" height="'+s+'" ')}</body></html>`);
 await p.screenshot({path:out+'/'+n,omitBackground:false,clip:{x:0,y:0,width:s,height:s}});}
await b.close()})();
