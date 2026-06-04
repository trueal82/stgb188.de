(function(){
  function showToast(message){
    var toast = document.querySelector('.copy-toast');
    if(!toast){
      toast = document.createElement('div');
      toast.className = 'copy-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(toast.hideTimeout);
    toast.hideTimeout = setTimeout(function(){
      toast.classList.remove('visible');
    }, 2200);
  }

  document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.snippet-box pre').forEach(function(pre){
      var btn = document.createElement('button');
      btn.textContent = 'Kopieren';
      btn.className = 'cta-button';
      pre.parentNode.insertBefore(btn, pre.nextSibling);
      btn.addEventListener('click', function(){
        var text = pre.textContent.trim();
        if(navigator.clipboard && navigator.clipboard.writeText){
          navigator.clipboard.writeText(text).then(function(){
            showToast('Text kopiert');
          }, function(){
            showToast('Kopieren nicht möglich');
          });
        } else {
          showToast('Kopieren nicht möglich');
        }
      });
    });
  });
})();
