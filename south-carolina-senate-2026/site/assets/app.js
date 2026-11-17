(function(){
  var body=document.body;
  function setMode(m){
    body.classList.remove('mode-en','mode-zh');
    if(m==='en')body.classList.add('mode-en');
    if(m==='zh')body.classList.add('mode-zh');
    document.querySelectorAll('.modes button').forEach(function(b){b.classList.toggle('on',b.dataset.mode===m)});
    try{localStorage.setItem('dsh-mode',m)}catch(e){}
  }
  document.querySelectorAll('.modes button').forEach(function(b){
    b.addEventListener('click',function(){setMode(b.dataset.mode)});
  });
  var saved='both'; try{saved=localStorage.getItem('dsh-mode')||'both'}catch(e){}
  setMode(saved);

  document.querySelectorAll('[data-facet-group]').forEach(function(group){
    var target=document.getElementById(group.dataset.facetGroup);
    if(!target) return;
    group.querySelectorAll('button').forEach(function(b){
      b.addEventListener('click',function(){
        group.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});
        var want=b.dataset.facet;
        target.querySelectorAll('[data-identity]').forEach(function(el){
          el.style.display=(want==='all'||el.dataset.identity===want)?'':'none';
        });
      });
    });
  });

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
})();
