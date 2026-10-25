const http=require('http'),fs=require('fs'),path=require('path'),{chromium}=require('playwright');
const root=__dirname;
const srv=http.createServer((q,s)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f,(e,d)=>{if(e){s.writeHead(404);s.end();return}
  s.writeHead(200,{'Content-Type':f.endsWith('.js')?'text/javascript':f.endsWith('.html')?'text/html':'application/octet-stream'});s.end(d)})}).listen(8765);
(async()=>{
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const scenes=JSON.parse(fs.readFileSync(process.argv[2]));
  for(const S of scenes){
    const p=await b.newPage({viewport:{width:S.w||1400,height:S.h||1000}});
    p.on('console',m=>console.log('page:',m.text())); p.on('pageerror',e=>console.log('err:',e.message));
    await p.goto('http://localhost:8765/page.html'); await p.waitForFunction('window.ready');
    await p.evaluate(s=>window.renderScene(s),S);
    await p.screenshot({path:S.out,clip:{x:0,y:0,width:S.w||1400,height:S.h||1000}}); console.log('wrote',S.out); await p.close();
  }
  await b.close(); srv.close();
})();
