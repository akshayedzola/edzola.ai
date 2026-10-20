(function(){
  'use strict';
  var canonical=document.querySelector('link[rel="canonical"]');
  var current=new URL(canonical&&canonical.href?canonical.href:window.location.href,window.location.href);
  var parts=current.pathname.split('/').filter(Boolean);
  var locale=parts[0]==='es'||parts[0]==='pt'?parts.shift():'en';
  if(parts[0]!=='verticals')return;
  var leaf=parts.slice(1).join('/');
  var copy={
    en:{home:'/',what:'What we do',verticals:'Verticals',all:'All verticals',programme:'Programme & evidence',funding:'Funding & relationships',people:'People & HR',finance:'Finance & operations',sectors:'Sectors',thinking:'Thinking',about:'About',talk:'Talk to us',menu:'Menu'},
    es:{home:'/es/',what:'Qué hacemos',verticals:'Verticales',all:'Todas las verticales',programme:'Programas y evidencia',funding:'Financiación y relaciones',people:'Personas y RR. HH.',finance:'Finanzas y operaciones',sectors:'Sectores',thinking:'Ideas',about:'Nosotros',talk:'Habla con nosotros',menu:'Menú'},
    pt:{home:'/pt/',what:'O que fazemos',verticals:'Verticais',all:'Todas as verticais',programme:'Programas e evidências',funding:'Captação e relacionamentos',people:'Pessoas e RH',finance:'Finanças e operações',sectors:'Setores',thinking:'Reflexões',about:'Sobre',talk:'Fale com a gente',menu:'Menu'}
  };
  var c=copy[locale];
  function route(lang){
    var prefix=lang==='en'?'/verticals/':'/'+lang+'/verticals/';
    return prefix+(leaf?leaf+'/':'');
  }
  var language='<a href="'+route('en')+'" hreflang="en" lang="en"'+(locale==='en'?' aria-current="true"':'')+'>EN</a>'
    +'<a href="'+route('es')+'" hreflang="es" lang="es"'+(locale==='es'?' aria-current="true"':'')+'>ES</a>'
    +'<a href="'+route('pt')+'" hreflang="pt" lang="pt"'+(locale==='pt'?' aria-current="true"':'')+'>PT</a>';
  var shell=document.querySelector('.nav-shell');
  var headerCta=shell&&shell.querySelector('.header-cta');
  if(shell&&headerCta&&!shell.querySelector(':scope > .nav-lang')){
    var nav=document.createElement('nav');
    nav.className='nav-lang';
    nav.setAttribute('aria-label',locale==='en'?'Language':'Idioma');
    nav.innerHTML=language;
    shell.insertBefore(nav,headerCta);
  }
  if(headerCta)headerCta.href='#contact-form';
  var menu=document.querySelector('.mobile-menu');
  var panel=menu&&menu.querySelector('.mobile-panel');
  if(menu){
    var menuSummary=menu.querySelector(':scope > summary');
    if(menuSummary)menuSummary.textContent=c.menu;
  }
  if(panel){
    var prefix=locale==='en'?'/verticals/':'/'+locale+'/verticals/';
    panel.innerHTML='<nav class="mobile-lang" aria-label="'+(locale==='en'?'Language':'Idioma')+'">'+language+'</nav>'
      +'<a href="'+c.home+'#model">'+c.what+'</a>'
      +'<details><summary>'+c.verticals+'</summary><a href="'+prefix+'">'+c.all+'</a><a href="'+prefix+'programme-evidence-systems/">'+c.programme+'</a><a href="'+prefix+'fundraising-donor-grant-systems/">'+c.funding+'</a><a href="'+prefix+'people-hr-systems/">'+c.people+'</a><a href="'+prefix+'finance-operations-systems/">'+c.finance+'</a></details>'
      +'<a href="/sectors/">'+c.sectors+'</a><a href="'+c.home+'impact-os/">ImpactOS</a><a href="/thinking/">'+c.thinking+'</a><a href="'+c.home+'about/">'+c.about+'</a><a href="#contact-form">'+c.talk+'</a>';
    panel.addEventListener('click',function(event){
      var link=event.target.closest('a');
      if(!link)return;
      var href=link.getAttribute('href')||'';
      if(href.charAt(0)==='#'){
        var target=document.querySelector(href);
        if(target){
          event.preventDefault();
          menu.open=false;
          window.requestAnimationFrame(function(){
            target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
            window.history.replaceState(null,'',href);
          });
          return;
        }
      }
      menu.open=false;
    });
  }
})();
