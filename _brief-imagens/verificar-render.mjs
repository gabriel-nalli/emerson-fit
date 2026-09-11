// Browser-only verification: local Chrome + native CDP, no image processing.
import { spawn } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const out = fileURLToPath(new URL('./verificacao/', import.meta.url));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
  '--no-default-browser-check', '--disable-background-networking',
  '--disable-component-update', '--disable-breakpad',
  `--user-data-dir=${out}chrome-profile`, '--remote-debugging-port=9335', 'about:blank',
], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let ws;
try {
  let pages;
  for (let i=0; i<50; i++) {
    try { pages = await (await fetch('http://localhost:9335/json/list')).json(); break; }
    catch { await sleep(200); }
  }
  if (!pages) throw Error('Chrome CDP did not start');
  ws = new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject;});
  let id=0;const pending=new Map();const errors=[];const responses=[];
  ws.onmessage=e=>{
    const m=JSON.parse(e.data);
    if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}
    if(m.method==='Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);
    if(m.method==='Network.responseReceived' && /ng-car|bg-biocarol/.test(m.params.response.url))
      responses.push({url:m.params.response.url,status:m.params.response.status});
  };
  const call=(method,params={})=>new Promise((resolve,reject)=>{
    pending.set(++id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));
  });
  const evaluate=async expression=>(await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result.value;
  await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
  await call('Network.setCacheDisabled',{cacheDisabled:true});
  const checks=[];
  for(const [device,width,height] of [['desktop',1440,900],['mobile',430,932]]){
    await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:device==='mobile'});
    await call('Page.navigate',{url:'http://localhost:5175/?foto-verificacao='+device});
    await sleep(3000);
    await evaluate('document.fonts.ready.then(()=>true)');
    for(const [section,selector] of [['topo','.elementor-element-4a8a6a40'],['sobre','.elementor-element-19cee890']]){
      await evaluate(`document.querySelector('${selector}').scrollIntoView({block:'start'})`);
      await sleep(2500);
      const info=await evaluate(`(()=>{const e=document.querySelector('${selector}'),r=e.getBoundingClientRect(),s=getComputedStyle(e);return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,background:s.backgroundImage,viewport:innerWidth,pageWidth:document.documentElement.scrollWidth}})()`);
      checks.push({device,section,...info});
      const options={format:'png',captureBeyondViewport:true,
        clip:{x:0,y:info.y,width:width,height:Math.ceil(info.height),scale:1}};
      const shot=await call('Page.captureScreenshot',options);
      await writeFile(out+`${section}-${device}.png`,Buffer.from(shot.data,'base64'));
    }
  }
  await writeFile(out+'render.json',JSON.stringify({checks,responses,errors},null,2));
  console.log(JSON.stringify({checks,responses,errors},null,2));
  await call('Browser.close');
} finally { if(ws)ws.close();chrome.kill('SIGTERM'); }
