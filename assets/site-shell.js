/* Behaviour for the shared edzola.ai header. The markup is rendered into each page by
   scripts/build-site-shell.mjs, so navigation works and is crawlable without this script. */
(function(){
  'use strict';
  if(window.__edzolaSiteShellInitialised)return;
  var header=document.querySelector('[data-ez-header]');
  if(!header)return;
  window.__edzolaSiteShellInitialised=true;

  var triggers=[].slice.call(header.querySelectorAll('[data-ez-trigger]'));
  var localeTrigger=header.querySelector('[data-ez-locale-trigger]');
  var localeMenu=header.querySelector('[data-ez-locale-menu]');
  var mobileToggle=header.querySelector('[data-ez-mobile-toggle]');
  var mobileNav=document.querySelector('[data-ez-mobile-nav]');
  var mobileLabel=header.querySelector('[data-ez-mobile-label]');
  var canHover=window.matchMedia('(hover:hover) and (pointer:fine)');
  var active=null,closeTimer=null,hoverTimer=null;

  function menuFor(name){return header.querySelector('[data-ez-menu="'+name+'"]')}
  function triggerFor(name){return header.querySelector('[data-ez-trigger="'+name+'"]')}

  function openMenu(name){
    if(active===name)return;
    closeMenus(false,true);closeLocale();
    var menu=menuFor(name);
    active=name;clearTimeout(closeTimer);
    triggerFor(name).setAttribute('aria-expanded','true');
    menu.hidden=false;
    requestAnimationFrame(function(){menu.classList.add('is-open')});
  }
  function closeMenus(returnFocus,immediate){
    var previous=active;
    triggers.forEach(function(t){t.setAttribute('aria-expanded','false')});
    [].forEach.call(header.querySelectorAll('[data-ez-menu]'),function(menu){
      if(!menu.classList.contains('is-open')&&menu.hidden)return;
      menu.classList.remove('is-open');
      if(immediate)menu.hidden=true;
      else setTimeout(function(){if(!menu.classList.contains('is-open'))menu.hidden=true},190);
    });
    active=null;
    if(returnFocus&&previous)triggerFor(previous).focus();
  }
  function closeLocale(){localeTrigger.setAttribute('aria-expanded','false');localeMenu.hidden=true}

  triggers.forEach(function(trigger){
    var name=trigger.getAttribute('data-ez-trigger');
    trigger.addEventListener('click',function(){if(active===name)closeMenus();else openMenu(name)});
    trigger.addEventListener('keydown',function(event){
      if(event.key==='ArrowDown'){event.preventDefault();openMenu(name);var first=menuFor(name).querySelector('a');if(first)first.focus()}
    });
    trigger.addEventListener('pointerenter',function(){
      if(!canHover.matches)return;
      clearTimeout(closeTimer);clearTimeout(hoverTimer);
      hoverTimer=setTimeout(function(){openMenu(name)},active?0:110);
    });
    trigger.addEventListener('pointerleave',function(){clearTimeout(hoverTimer)});
  });
  header.addEventListener('pointerleave',function(){
    if(!canHover.matches||!active)return;
    clearTimeout(hoverTimer);
    closeTimer=setTimeout(function(){closeMenus()},260);
  });
  header.addEventListener('pointerenter',function(){clearTimeout(closeTimer)});
  /* Leaving a menu with Tab closes it so it never hides the content being focused. */
  header.addEventListener('focusout',function(event){
    if(active&&event.relatedTarget&&!header.contains(event.relatedTarget))closeMenus();
  });

  localeTrigger.addEventListener('click',function(){
    var open=localeTrigger.getAttribute('aria-expanded')!=='true';
    closeMenus(false,true);
    localeTrigger.setAttribute('aria-expanded',String(open));
    localeMenu.hidden=!open;
  });

  function setMobileTop(){mobileNav.style.setProperty('--ez-mobile-top',Math.max(0,Math.round(header.getBoundingClientRect().bottom))+'px')}
  function closeMobile(returnFocus){
    if(mobileToggle.getAttribute('aria-expanded')!=='true')return;
    mobileToggle.setAttribute('aria-expanded','false');
    mobileLabel.textContent=mobileLabel.getAttribute('data-closed');
    document.body.classList.remove('ez-nav-open');
    mobileNav.hidden=true;
    if(returnFocus)mobileToggle.focus();
  }
  mobileToggle.addEventListener('click',function(){
    if(mobileToggle.getAttribute('aria-expanded')==='true'){closeMobile();return}
    closeMenus(false,true);closeLocale();setMobileTop();
    mobileToggle.setAttribute('aria-expanded','true');
    mobileLabel.textContent=mobileLabel.getAttribute('data-open');
    document.body.classList.add('ez-nav-open');
    mobileNav.hidden=false;
  });
  mobileNav.addEventListener('click',function(event){if(event.target===mobileNav||event.target.closest('a'))closeMobile()});

  document.addEventListener('pointerdown',function(event){
    if(!header.contains(event.target)){closeMenus();closeLocale()}
  });
  document.addEventListener('keydown',function(event){
    if(event.key!=='Escape')return;
    if(mobileToggle.getAttribute('aria-expanded')==='true')closeMobile(true);
    else if(localeTrigger.getAttribute('aria-expanded')==='true'){closeLocale();localeTrigger.focus()}
    else if(active)closeMenus(true);
  });
  window.addEventListener('resize',function(){if(window.innerWidth>1080)closeMobile();else closeMenus(false,true)});

  var scrolled=false;
  function onScroll(){var next=window.scrollY>8;if(next!==scrolled){scrolled=next;header.classList.toggle('is-scrolled',next)}}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
})();
