
(function(){
  var body=document.body;
  function setMode(m){
    body.classList.remove('mode-en','mode-zh');
    if(m==='en')body.classList.add('mode-en');
    if(m==='zh')body.classList.add('mode-zh');
    document.querySelectorAll('.modes button').forEach(function(b){b.classList.toggle('on',b.dataset.mode===m)});
    try{localStorage.setItem('dsh-mode',m)}catch(e){}
  }
  document.querySelectorAll('.modes button').forEach(function(b){b.addEventListener('click',function(){setMode(b.dataset.mode)})});
  var saved='both'; try{saved=localStorage.getItem('dsh-mode')||'both'}catch(e){}
  setMode(saved);

  // table filter
  document.querySelectorAll('[data-filter]').forEach(function(inp){
    var tbl=document.getElementById(inp.dataset.filter);
    if(!tbl)return;
    inp.addEventListener('input',function(){
      var q=inp.value.toLowerCase();
      tbl.querySelectorAll('tbody tr').forEach(function(tr){
        tr.style.display=tr.textContent.toLowerCase().indexOf(q)>-1?'':'none';
      });
    });
  });

  // search
  var box=document.getElementById('q'), res=document.getElementById('results');
  if(box&&res&&window.SEARCH_INDEX){
    var timer=null;
    function run(){
      var q=box.value.trim().toLowerCase();
      if(q.length<2){res.innerHTML='<div class="hit"><div class="s">输入至少 2 个字符开始检索 / Type at least 2 characters.</div></div>';return;}
      var hits=[];
      SEARCH_INDEX.forEach(function(e){
        var hay=(e.t+' '+e.b).toLowerCase();
        var i=hay.indexOf(q);
        if(i>-1){
          var start=Math.max(0,i-40), frag=e.b.substr(start,150);
          hits.push({t:e.t,u:e.u,b:frag,n:e.n});
        }
      });
      hits=hits.slice(0,40);
      if(!hits.length){res.innerHTML='<div class="hit"><div class="s">没有匹配项 / No matches.</div></div>';return;}
      res.innerHTML=hits.map(function(h){
        var safe=h.b.replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]});
        var re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');
        safe=safe.replace(re,'<mark>$1</mark>');
        return '<a class="hit" href="'+h.u+'"><div class="t">'+h.t+'</div><div class="s">'+h.n+' · '+safe+'…</div></a>';
      }).join('');
    }
    box.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(run,120)});
  }
})();
