/* Homepage behaviour: the "Happening now" spotlight, the solutions explorer, the logo band pause control and the
   partner video player. Everything is usable without this script: the first spotlight panel
   is visible, logos render statically and video cards fall back to their thumbnails. */
(function(){
  'use strict';
  var reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Spotlight: tabs that advance on their own, pause on hover, focus or the pause button,
     and never move when the visitor prefers reduced motion. */
  var spotlight=document.querySelector('[data-spotlight]');
  if(spotlight){
    var tabs=[].slice.call(spotlight.querySelectorAll('[data-spot-tab]'));
    var pause=spotlight.querySelector('[data-spot-pause]');
    var DURATION=9000,current=0,timer=null,paused=reduceMotion,held=false;

    function show(index,moveFocus){
      current=(index+tabs.length)%tabs.length;
      tabs.forEach(function(tab,i){
        var active=i===current;
        tab.setAttribute('aria-selected',String(active));
        tab.tabIndex=active?0:-1;
        document.getElementById(tab.getAttribute('aria-controls')).hidden=!active;
      });
      if(moveFocus)tabs[current].focus();
      restart();
    }
    function restart(){
      clearTimeout(timer);
      spotlight.classList.remove('is-running');
      if(paused||held)return;
      void spotlight.offsetWidth; /* restart the progress bar animation */
      spotlight.style.setProperty('--spot-duration',DURATION+'ms');
      spotlight.classList.add('is-running');
      timer=setTimeout(function(){show(current+1)},DURATION);
    }
    function setPaused(next){
      paused=next;
      pause.setAttribute('aria-pressed',String(paused));
      pause.textContent=paused?'Play':'Pause';
      restart();
    }

    tabs.forEach(function(tab,i){
      tab.addEventListener('click',function(){show(i)});
      tab.addEventListener('keydown',function(event){
        var step={ArrowRight:1,ArrowLeft:-1}[event.key];
        if(event.key==='Home'){event.preventDefault();show(0,true)}
        else if(event.key==='End'){event.preventDefault();show(tabs.length-1,true)}
        else if(step){event.preventDefault();show(i+step,true)}
      });
    });
    pause.addEventListener('click',function(){setPaused(!paused)});
    spotlight.addEventListener('pointerenter',function(){held=true;restart()});
    spotlight.addEventListener('pointerleave',function(){held=false;restart()});
    spotlight.addEventListener('focusin',function(){held=true;restart()});
    spotlight.addEventListener('focusout',function(event){if(!spotlight.contains(event.relatedTarget)){held=false;restart()}});
    document.addEventListener('visibilitychange',function(){held=document.hidden;restart()});
    if(reduceMotion)setPaused(true);else restart();
  }

  /* Solutions explorer: a plain tab list. No auto-rotation; the visitor chooses. */
  var explorer=document.querySelector('[data-explorer]');
  if(explorer){
    var exTabs=[].slice.call(explorer.querySelectorAll('[data-ex-tab]'));
    var select=function(index,moveFocus){
      index=(index+exTabs.length)%exTabs.length;
      exTabs.forEach(function(tab,i){
        var active=i===index;
        tab.setAttribute('aria-selected',String(active));
        tab.tabIndex=active?0:-1;
        document.getElementById(tab.getAttribute('aria-controls')).hidden=!active;
      });
      if(moveFocus)exTabs[index].focus();
    };
    exTabs.forEach(function(tab,i){
      tab.addEventListener('click',function(){select(i)});
      tab.addEventListener('keydown',function(event){
        var step={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[event.key];
        if(event.key==='Home'){event.preventDefault();select(0,true)}
        else if(event.key==='End'){event.preventDefault();select(exTabs.length-1,true)}
        else if(step){event.preventDefault();select(i+step,true)}
      });
    });
  }

  /* Logo band pause control (motion longer than five seconds must be stoppable). */
  var logoPause=document.querySelector('[data-logo-pause]');
  if(logoPause){
    var band=logoPause.closest('.logo-band');
    logoPause.addEventListener('click',function(){
      var isPaused=band.classList.toggle('is-paused');
      logoPause.setAttribute('aria-pressed',String(isPaused));
      logoPause.textContent=isPaused?'Play logos':'Pause logos';
    });
  }

  /* Partner videos open in a dialog; YouTube only loads after the visitor asks for it. */
  var modal=document.getElementById('video-modal');
  if(modal&&typeof modal.showModal==='function'){
    var frame=modal.querySelector('.video-frame');
    var opener=null;
    document.querySelectorAll('[data-video]').forEach(function(button){
      button.addEventListener('click',function(){
        var iframe=document.createElement('iframe');
        iframe.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(button.getAttribute('data-video'))+'?autoplay=1&rel=0&playsinline=1';
        iframe.title=button.getAttribute('aria-label').replace(/^Play video: /,'');
        iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen=true;
        frame.replaceChildren(iframe);
        opener=button;
        modal.showModal();
      });
    });
    modal.querySelector('.video-close').addEventListener('click',function(){modal.close()});
    modal.addEventListener('click',function(event){if(event.target===modal)modal.close()});
    modal.addEventListener('close',function(){frame.replaceChildren();if(opener)opener.focus()});
  }else{
    document.querySelectorAll('[data-video]').forEach(function(button){
      button.addEventListener('click',function(){window.open('https://www.youtube.com/watch?v='+encodeURIComponent(button.getAttribute('data-video')),'_blank','noopener')});
    });
  }
})();
