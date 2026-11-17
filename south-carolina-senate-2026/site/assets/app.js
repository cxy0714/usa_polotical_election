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
