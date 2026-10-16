(function(){
  'use strict';
  if(window.__edzolaCrmFormInitialised)return;

  var canonical=document.querySelector('link[rel="canonical"]');
  var landingUrl=canonical&&canonical.href?canonical.href:(window.location.origin+window.location.pathname);
  var path=(new URL(landingUrl,window.location.href).pathname);
  var slug=(path.split('/').filter(Boolean)[0]||'home');
  var contextKey=path.indexOf('/team/impactos/')===0?'impactos':(path==='/zolabs/why/'?'why':slug);
  var formContexts={
    'home':{
      title:'Start with one part of the work that feels harder than it should.',
      body:'Bring one tracker, form or workflow. We’ll help you find a practical first step—whether that means a clearer process, a connected system or better use of what you already have.'
    },
    'dozai':{
      title:'Bring us one workflow where AI might help.',
      body:'Tell us what your team is trying to decide or do. We’ll help you judge whether AI is useful, what a safe pilot looks like and where people must stay in control.'
    },
    'zolabs':{
      title:'Tell us what you need to learn from people’s voices.',
      body:'Share the study, feedback exercise or evaluation you have in mind. We’ll help you shape a small multilingual voice-research pilot.'
    },
    'zolashield':{
      title:'Tell us where data protection feels unclear.',
      body:'Share the kind of personal data your organisation handles and where it is stored. We’ll help you identify a practical first step towards DPDP readiness.'
    },
    'patrons':{
      title:'Tell us how you would like to support the Built for Impact Programme.',
      body:'You can sponsor a nonprofit, contribute implementation time or offer technology credits. We’ll help match your support to a concrete need.'
    },
    'impactos':{
      title:'Tell us which part of ImpactOS you want to explore.',
      body:'Share the programme or organisational workflow you want to strengthen. We’ll help identify the smallest useful module to begin with.'
    },
    'impact-os':{
      title:'Tell us what your programme system needs to make clearer.',
      body:'Share the programme model, the decisions your team needs to make and one tracker you use today. We’ll help identify the smallest useful blueprint to begin with.'
    },
    'fundzola':{
      title:'Tell us what your finance team needs to see more clearly.',
      body:'Share how you manage grants, budgets and donor reporting today. We’ll help you identify a practical first step without disrupting the tools you already use.'
    },
    'thinking':{
      title:'Bring us a question from the work.',
      body:'If something here connects with a challenge your team is facing, tell us what is happening now. We’ll help you think through a practical next step.'
    },
    'why':{
      title:'Tell us what better technology should make possible for your team.',
      body:'Start with the mission, the people doing the work and one process that is getting in their way. We’ll help you work backwards to a useful first step.'
    },
    'field-guides':{
      title:'Tell us where technology is not sticking.',
      body:'Bring one tracker, tool or handoff that your team is struggling with. We’ll help you find a first version people can actually use.'
    }
  };
  var context=formContexts[contextKey]||formContexts.home;

  function createFormHost(){
    var section=document.createElement('section');
    section.className='crm-embed-section';
    section.setAttribute('aria-labelledby','crm-embed-heading');
    section.innerHTML='<div class="crm-embed-inner"><div class="final"><div><h2 id="crm-embed-heading">'+context.title+'</h2><p>'+context.body+'</p></div><div class="contact" data-crm-webform><div class="alt"><b>Explore first</b><a href="/sectors/">Browse the sector playbooks →</a><a href="/thinking/">Read how EdZola approaches the work →</a></div></div></div></div>';
    var footer=document.querySelector('footer');
    if(footer)footer.parentNode.insertBefore(section,footer);
    else document.body.appendChild(section);
    return section.querySelector('[data-crm-webform]');
  }

  var contact=document.querySelector('[data-crm-webform], #talk .contact');
  if(!contact)contact=createFormHost();
  if(!contact)return;
  window.__edzolaCrmFormInitialised=true;
  if(document.querySelector('link[href*="sector-playbook.css"]')||contextKey==='sectors'||contextKey==='contact'){
    document.documentElement.setAttribute('data-theme','light');
  }

  var finalPanel=contact.closest('.final');
  var intro=finalPanel&&finalPanel.firstElementChild;
  if(finalPanel)finalPanel.classList.add('crm-final');
  if(intro){
    intro.classList.add('crm-intro');
    if(!intro.querySelector('.form-kicker')){
      var kicker=document.createElement('span');
      kicker.className='form-kicker';
      kicker.textContent='Start with the work, not the software';
      intro.insertBefore(kicker,intro.firstChild);
    }
    if(!intro.querySelector('.form-points')){
      var points=document.createElement('ul');
      points.className='form-points';
      points.innerHTML='<li>Start with one spreadsheet, form or process that is slowing the team down.</li><li>The first walkthrough is free and takes about 30 minutes.</li><li>If budget is tight, ask about the Built for Impact Programme.</li>';
      intro.appendChild(points);
    }
  }

  var alt=contact.querySelector('.crm-alt,.alt');
  var altHtml=alt?alt.innerHTML:'<b>Not ready to get in touch yet?</b><a href="/sectors/">Browse all sector playbooks →</a><a href="/thinking/">Read how EdZola approaches the work →</a>';
  var examples={
    'home':'we have a process that depends on several trackers, and the team cannot see what needs attention next.',
    'sectors':'we are not sure which programme model best fits our work, or what the first useful system should track.',
    'education':'attendance sits in five spreadsheets, and we cannot see which learners need a follow-up.',
    'youth-employability':'placements are recorded, but we cannot see who is still in work after three or six months.',
    'livelihoods':'household support, enterprise milestones and scheme applications sit in separate trackers.',
    'health':'referrals and follow-ups are spread across paper registers, WhatsApp and facility reports.',
    'mental-health':'screening, intake and continuing-care follow-ups are difficult to connect safely.',
    'maternal-child-health':'pregnancy, referral, birth and postnatal follow-ups are tracked by different teams.',
    'child-protection':'case actions, referrals and review deadlines are difficult to follow across partners.',
    'gender':'we count activities, but cannot easily see whether women gained choice, safety or control.',
    'disability':'assessments, accommodations and service referrals are held in different places.',
    'justice':'case deadlines, referrals and whether a remedy was enforced are difficult to follow.',
    'environment':'field activity, community ownership and ecological outcomes sit in separate reports.',
    'waste':'collection, material recovery and worker payments do not reconcile across sites.',
    'food-systems':'farmer support, procurement and nutrition outcomes are tracked in separate systems.',
    'community-development':'village plans, participation and action follow-up are difficult to connect.',
    'media':'tips, reporting, publication and the change that followed are held in different tools.',
    'arts':'applications, participation, grants and artist outcomes are difficult to follow over time.',
    'dozai':'we want to test whether AI can reduce a repetitive task without losing human review.',
    'zolabs':'we need to collect and understand multilingual interviews or programme feedback at scale.',
    'zolashield':'we hold personal data in several tools and need a practical path towards DPDP readiness.',
    'patrons':'we would like to support a nonprofit with technology credits, implementation funding or expertise.',
    'impactos':'we want to connect one programme workflow without trying to replace every tool at once.',
    'impact-os':'we need a programme blueprint that connects delivery, follow-up and reporting around how our work actually runs.',
    'fundzola':'grant budgets, spending and donor reports take too much manual reconciliation each month.',
    'thinking':'one of our programme processes is not working as clearly as it should.',
    'why':'technology is adding work for our team instead of helping them make better decisions.',
    'field-guides':'a tool or workflow was introduced, but the team is struggling to use it consistently.',
    'contact':'our team spends too much time reconciling trackers and still cannot see what needs attention.'
  };

  contact.classList.add('contact','crm-contact');
  contact.id='contact-form';
  contact.innerHTML=''
    +'<h3 class="form-title">Tell us a little about your work.</h3>'
    +'<p class="form-note">Five short questions. Plain language is perfect; you do not need to have the solution worked out.</p>'
    +'<div id="crmWebToEntityForm" class="zcwf_lblLeft crmWebToEntityForm">'
    +'<div class="wf_customMessageBox" id="wf_splash" style="display:none"><div class="wf_customCircle"><div class="wf_customCheckMark"></div></div><span id="wf_splash_info"></span></div>'
    +'<form id="webform4805054000017631043" name="WebToLeads4805054000017631043" accept-charset="UTF-8" novalidate>'
    +'<input type="hidden" name="xnQsjsdp" value="1aade6b3cf8605c22d9acb6ee15fe0c428d2691bb6cf81fb9b3d225fdc32db68">'
    +'<input type="hidden" name="zc_gad" id="zc_gad" value="">'
    +'<input type="hidden" name="xmIwtLD" value="3b79072affb4a67d4ba6bb28b81a6a3d0aa0725f4c8cad64a6070747b18b1cb86d26b59432bd3601ee65f8da8a548744">'
    +'<input type="hidden" name="actionType" value="TGVhZHM=">'
    +'<input type="hidden" name="returnURL" value="null">'
    +'<!-- Do not remove this code. -->'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Last_Name">Your name <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="text" id="Last_Name" aria-required="true" name="Last Name" maxlength="80" autocomplete="name" placeholder="For example, Asha Menon"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Company">Organisation name <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="text" id="Company" aria-required="true" name="Company" maxlength="200" autocomplete="organization" placeholder="Your nonprofit or organisation"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Email">Work email <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="email" ftype="email" id="Email" aria-required="true" name="Email" maxlength="100" autocomplete="email" placeholder="you@yourorganisation.org"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="LEADCF41">What would you like help with? <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><select class="zcwf_col_fld_slt" id="LEADCF41" aria-required="true" name="LEADCF41"><option value="-None-">Choose the closest option</option><option value="Data Systems – MIS / ERP">A programme data system or MIS</option><option value="CRM">Managing partners, donors or relationships</option><option value="HRMS">People and HR systems</option><option value="zolabs.ai – Qualitative Data Collection">Understanding interviews and qualitative data</option><option value="zolashield – DPDP Compliance">Data protection and DPDP readiness</option><option value="Custom AI Solutions">A custom AI solution</option><option value="AI Workshops and Advisory">AI workshops or advice</option><option value="Built for Impact program">The Built for Impact Programme</option></select></div></div>'
    +'<input type="hidden" id="LEADCF121" name="LEADCF121" value="">'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="LEADCF40">What is getting in the way today? <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><textarea id="LEADCF40" aria-required="true" name="LEADCF40" placeholder="For example: '+(examples[contextKey]||examples.contact)+'"></textarea></div></div>'
    +'<input type="hidden" name="aG9uZXlwb3Q" value="" tabindex="-1" autocomplete="off">'
    +'<div class="form-actions"><input type="submit" id="formsubmit" class="formsubmit zcwf_button" value="Tell us about your work" aria-label="Tell us about your work"><input type="reset" class="zcwf_button formreset" value="Clear" aria-label="Clear form"></div>'
    +'<p class="privacy-note">Your details go directly to EdZola’s CRM so our team can respond to this enquiry.</p><p class="form-status" id="crm-form-status" role="status" aria-live="polite"></p>'
    +'</form></div><div class="crm-alt">'+altHtml+'</div>';

  var form=document.getElementById('webform4805054000017631043');
  var status=document.getElementById('crm-form-status');
  var landingField=document.getElementById('LEADCF121');
  landingField.value=landingUrl;
  var helpField=document.getElementById('LEADCF41');
  var helpDefaults={
    'dozai':'Custom AI Solutions',
    'zolabs':'zolabs.ai – Qualitative Data Collection',
    'zolashield':'zolashield – DPDP Compliance',
    'patrons':'Built for Impact program',
    'impactos':'Data Systems – MIS / ERP',
    'impact-os':'Data Systems – MIS / ERP',
    'fundzola':'Data Systems – MIS / ERP'
  };
  if(helpDefaults[contextKey])helpField.value=helpDefaults[contextKey];

  function showStatus(message,isError){
    status.textContent=message;
    status.classList.toggle('error',!!isError);
  }
  function validEmail(field){
    var value=field.value.trim(),at=value.indexOf('@'),dot=value.lastIndexOf('.');
    return value&&at>0&&dot>at+1&&dot+2<value.length;
  }
  function mandatoryFieldsPresent(){
    var fields=['Last Name','Company','Email','LEADCF41','LEADCF40'];
    var labels=['your name','your organisation name','your work email','what you would like help with','what is getting in the way today'];
    for(var i=0;i<fields.length;i++){
      var field=form.elements[fields[i]];
      if(!field||!String(field.value).trim()||(field.tagName==='SELECT'&&field.value==='-None-')){
        showStatus('Please complete '+labels[i]+'.',true);
        if(field)field.focus();
        return false;
      }
    }
    if(!validEmail(form.elements.Email)){
      showStatus('Please enter a valid work email address.',true);
      form.elements.Email.focus();
      return false;
    }
    return true;
  }

  form.addEventListener('reset',function(){
    window.setTimeout(function(){landingField.value=landingUrl;showStatus('',false)},0);
  });
  form.addEventListener('submit',function(event){
    event.preventDefault();
    showStatus('',false);
    landingField.value=landingUrl;
    if(!mandatoryFieldsPresent())return;
    if(typeof _wfa_track!=='undefined'&&_wfa_track.wfa_submit)_wfa_track.wfa_submit(event);
    var button=form.querySelector('.formsubmit');
    button.disabled=true;
    button.value='Sending…';
    fetch('https://crm.zoho.com/crm/WebToLeadForm',{method:'POST',body:new FormData(form),cache:'no-cache'})
      .then(function(response){var type=response.headers.get('Content-Type')||'';return type.indexOf('application/json')>-1?response.json():response.text()})
      .then(function(data){
        if(typeof data==='object'&&data.invalidCaptcha==='true'){
          showStatus(data.actionvalue||'Please complete the security check and try again.',true);
          return;
        }
        if(typeof data==='object'&&data.redirectUrl){window.location.assign(data.redirectUrl);return;}
        if(typeof data==='object'&&data.message&&data.actionsubmit==='error_msg'){
          showStatus(data.message,true);
          return;
        }
        var message=document.getElementById('wf_splash_info');
        var splash=document.getElementById('wf_splash');
        var confirmation=typeof data==='object'&&data.actionvalue?data.actionvalue:'Thank you. Your note has been sent.';
        message.textContent=confirmation;
        splash.style.display='flex';
        HTMLFormElement.prototype.reset.call(form);
        showStatus(confirmation,false);
        window.setTimeout(function(){splash.style.display='none'},5000);
        if(typeof _wfa_track!=='undefined'&&_wfa_track.wfa_post_submit)_wfa_track.wfa_post_submit(event);
      })
      .catch(function(){showStatus('We could not send the form just now. Please try again in a moment.',true)})
      .finally(function(){button.disabled=false;button.value='Tell us about your work'});
  });

  if(typeof _wfa_fstprtcken==='undefined')window._wfa_fstprtcken={};
  window._wfa_fstprtcken[4805054000017631043]=true;

  document.querySelectorAll('a[href^="mailto:reachus@edzola.com"],a[href="/contact/"]').forEach(function(link){
    link.href='#contact-form';
    if(link.textContent.trim()==='reachus@edzola.com')link.textContent='Contact EdZola';
  });

  function loadAnalytics(){
    if(document.getElementById('wf_anal'))return;
    var analytics=document.createElement('script');
    analytics.id='wf_anal';
    analytics.src='https://crm.zohopublic.com/crm/WebFormAnalyticsServeServlet?rid=72503cf530bb7108b4b9b5e015423d195703075e3ec652764d0933ed977c0be23dd868dba5ccd31094239d28bb209238gidf136092d1e25e3382d7fd13d96d296b34ec0bce5df51b37a63c789bc0c29f50dgidae350f91e94d95b6cabcb6d9934e9b6dca5a26df4f358e7ed4edaa1e15619803gidc06e6b9fd3da2608c53a1f119611c8e1ffde579f4a6efa7f9603e5cbec4e1485&tw=3b6d1e8ae8dd0638bab7966561b498e5a4e6be03a837aede4cdfdade6945afd2&version=v2';
    document.body.appendChild(analytics);
  }

  /* Zoho's helper returns a document.write call. Capture its rotating token so
     the helper can be loaded safely after the page has finished parsing. */
  var originalWrite=document.write;
  document.write=function(markup){
    var value=String(markup).match(/elm\.value='([^']+)'/);
    if(!value||form.elements.Zm9ybWZpbGxpbmd0aW1l)return;
    var field=document.createElement('input');
    field.type='hidden';
    field.name='Zm9ybWZpbGxpbmd0aW1l';
    field.value=value[1];
    form.appendChild(field);
  };
  var servlet=document.createElement('script');
  servlet.src='https://crm.zohopublic.com/crm/WebFormServlet?rid=63c762ec700c7fb69bc5e1275ffc37f7cf92cbf45748de086117a2cb5c386dec';
  servlet.addEventListener('load',function(){document.write=originalWrite;loadAnalytics()});
  servlet.addEventListener('error',function(){document.write=originalWrite;loadAnalytics()});
  document.body.appendChild(servlet);
})();
