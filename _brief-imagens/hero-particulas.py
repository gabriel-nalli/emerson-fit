p='index.html'; s=open(p,encoding='utf-8').read()
assert 'hero-particles' not in s
css='''
/* depoimentos: cards sem fotos de alunos antigos (cliente ainda vai enviar as fotos) */
.elementor-element-3f555a78,.elementor-element-6c408a37,.elementor-element-327b9299{background-image:none!important;background:linear-gradient(160deg,#1d1d1d 0%,#0d0d0d 100%)!important;border:1px solid #262626!important}
.elementor-element-3f555a78 .elementor-icon-box-title,.elementor-element-6c408a37 .elementor-icon-box-title,.elementor-element-327b9299 .elementor-icon-box-title{color:#cefb69}
/* hero: partículas cinzas */
.elementor-element-4a8a6a40{position:relative;overflow:hidden}
.elementor-element-4a8a6a40>.e-con-inner{position:relative;z-index:1}
.hero-particles{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;display:block}
</style>'''
s=s.replace('</style>\n</head>',css+'\n</head>',1)
js='''<script id="hero-particles-js">
(function(){
  var host=document.querySelector('.elementor-element-4a8a6a40'); if(!host) return;
  var c=document.createElement('canvas'); c.className='hero-particles'; c.setAttribute('aria-hidden','true');
  host.insertBefore(c,host.firstChild);
  var ctx=c.getContext('2d'), dpr=Math.min(window.devicePixelRatio||1,2), W=0,H=0, pts=[], raf=0;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function resize(){
    W=host.clientWidth; H=host.clientHeight; c.width=W*dpr; c.height=H*dpr; c.style.width=W+'px'; c.style.height=H+'px';
    ctx.setTransform(dpr,0,0,dpr,0,0);
    var n=Math.round(Math.min(110,Math.max(40,W*H/16000)));
    pts=[]; for(var i=0;i<n;i++) pts.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.25,vy:(Math.random()-.5)*.25,r:Math.random()*1.6+.6,a:Math.random()*.5+.25});
  }
  function frame(){
    ctx.clearRect(0,0,W,H);
    var g=ctx.createRadialGradient(W*.18,H*.28,0,W*.18,H*.28,Math.max(W,H)*.6);
    g.addColorStop(0,'rgba(190,190,190,0.10)'); g.addColorStop(1,'rgba(190,190,190,0)');
    ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
    var L=Math.min(130,W*.11);
    for(var i=0;i<pts.length;i++){
      var p=pts[i];
      if(!reduce){ p.x+=p.vx; p.y+=p.vy; if(p.x<-10)p.x=W+10; if(p.x>W+10)p.x=-10; if(p.y<-10)p.y=H+10; if(p.y>H+10)p.y=-10; }
      for(var j=i+1;j<pts.length;j++){
        var q=pts[j], dx=p.x-q.x, dy=p.y-q.y, d=Math.sqrt(dx*dx+dy*dy);
        if(d<L){ ctx.strokeStyle='rgba(200,200,200,'+(0.16*(1-d/L)).toFixed(3)+')'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke(); }
      }
      ctx.fillStyle='rgba(215,215,215,'+p.a.toFixed(2)+')'; ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
    }
    if(!reduce) raf=requestAnimationFrame(frame);
  }
  resize(); frame();
  var t; window.addEventListener('resize',function(){clearTimeout(t); t=setTimeout(function(){resize(); if(reduce) frame();},150);});
  document.addEventListener('visibilitychange',function(){ if(reduce) return; if(document.hidden){cancelAnimationFrame(raf);} else {raf=requestAnimationFrame(frame);} });
})();
</script>
</body>'''
i=s.rfind('</body>'); s=s[:i]+js+s[i+len('</body>'):]
open(p,'w',encoding='utf-8').write(s); print('ok')
