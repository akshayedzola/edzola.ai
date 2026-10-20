(function(){
  'use strict';
  if(window.__edzolaCrmFormInitialised)return;

  var canonical=document.querySelector('link[rel="canonical"]');
  var landingUrl=canonical&&canonical.href?canonical.href:(window.location.origin+window.location.pathname);
  var path=(new URL(landingUrl,window.location.href).pathname);
  var parts=path.split('/').filter(Boolean);
  var locale=parts[0]==='es'||parts[0]==='pt'?parts.shift():'en';
  var translations={
    en:{formTitle:'Tell us a little about your work.',formNote:'Five short questions. Plain language is perfect; you do not need to have the solution worked out.',submit:'Tell us about your work',name:'Your name',namePlaceholder:'For example, Asha Menon',organisation:'Organisation name',organisationPlaceholder:'Your nonprofit or organisation',email:'Work email',help:'What would you like help with?',choose:'Choose the closest option',programme:'A programme data system or MIS',relationships:'Managing partners, donors or relationships',people:'People and HR systems',research:'Understanding interviews and qualitative data',protection:'Data protection and DPDP readiness',customAi:'A custom AI solution',aiAdvice:'AI workshops or advice',builtForImpact:'The Built for Impact Programme',barrier:'What is getting in the way today?',example:'For example: ',clear:'Clear',clearForm:'Clear form',privacy:'Your details go directly to EdZola’s CRM so our team can respond to this enquiry.',kicker:'Start with the work, not the software',points:['Start with one spreadsheet, form or process that is slowing the team down.','The first walkthrough is free and takes about 30 minutes.','If budget is tight, ask about the Built for Impact Programme.'],explore:'Not ready to get in touch yet?',browseSectors:'Browse all sector playbooks →',readApproach:'Read how EdZola approaches the work →',required:['your name','your organisation name','your work email','what you would like help with','what is getting in the way today'],complete:'Please complete ',validEmail:'Please enter a valid work email address.',sending:'Sending…',captcha:'Please complete the security check and try again.',thanks:'Thank you. Your note has been sent.',failed:'We could not send the form just now. Please try again in a moment.',contact:'Contact EdZola'},
    es:{formTitle:'Cuéntanos un poco sobre tu trabajo.',formNote:'Cinco preguntas breves. Puedes responder con palabras sencillas; no necesitas tener la solución definida.',submit:'Cuéntanos sobre tu trabajo',name:'Tu nombre',namePlaceholder:'Por ejemplo, Asha Menon',organisation:'Nombre de la organización',organisationPlaceholder:'Tu organización sin fines de lucro',email:'Correo de trabajo',help:'¿Con qué te gustaría recibir ayuda?',choose:'Elige la opción más cercana',programme:'Un sistema de datos de programas o MIS',relationships:'Gestión de aliados, donantes o relaciones',people:'Sistemas de personas y RR. HH.',research:'Comprender entrevistas y datos cualitativos',protection:'Protección de datos y preparación para DPDP',customAi:'Una solución de IA a medida',aiAdvice:'Talleres o asesoría sobre IA',builtForImpact:'El programa Built for Impact',barrier:'¿Qué está dificultando el trabajo hoy?',example:'Por ejemplo: ',clear:'Borrar',clearForm:'Borrar formulario',privacy:'Tus datos van directamente al CRM de EdZola para que nuestro equipo pueda responder a esta consulta.',kicker:'Empieza por el trabajo, no por el software',points:['Empieza con una hoja, formulario o proceso que esté frenando al equipo.','La primera conversación es gratuita y dura unos 30 minutos.','Si el presupuesto es limitado, pregunta por el programa Built for Impact.'],explore:'¿Todavía no quieres ponerte en contacto?',browseSectors:'Explora los itinerarios por sector →',readApproach:'Lee cómo aborda EdZola el trabajo →',required:['tu nombre','el nombre de tu organización','tu correo de trabajo','el tipo de ayuda que buscas','lo que dificulta el trabajo hoy'],complete:'Completa ',validEmail:'Introduce un correo de trabajo válido.',sending:'Enviando…',captcha:'Completa la verificación de seguridad e inténtalo de nuevo.',thanks:'Gracias. Hemos recibido tu mensaje.',failed:'No pudimos enviar el formulario. Inténtalo de nuevo en un momento.',contact:'Contactar con EdZola'},
    pt:{formTitle:'Conte um pouco sobre o seu trabalho.',formNote:'Cinco perguntas breves. Pode responder em linguagem simples; não precisa ter a solução pronta.',submit:'Conte sobre o seu trabalho',name:'Seu nome',namePlaceholder:'Por exemplo, Asha Menon',organisation:'Nome da organização',organisationPlaceholder:'Sua organização sem fins lucrativos',email:'E-mail de trabalho',help:'Em que você gostaria de receber ajuda?',choose:'Escolha a opção mais próxima',programme:'Um sistema de dados de programas ou MIS',relationships:'Gestão de parceiros, doadores ou relacionamentos',people:'Sistemas de pessoas e RH',research:'Compreender entrevistas e dados qualitativos',protection:'Proteção de dados e preparação para DPDP',customAi:'Uma solução de IA sob medida',aiAdvice:'Oficinas ou consultoria sobre IA',builtForImpact:'O programa Built for Impact',barrier:'O que está dificultando o trabalho hoje?',example:'Por exemplo: ',clear:'Limpar',clearForm:'Limpar formulário',privacy:'Seus dados vão diretamente para o CRM da EdZola para que nossa equipe possa responder a esta consulta.',kicker:'Comece pelo trabalho, não pelo software',points:['Comece com uma planilha, formulário ou processo que esteja atrasando a equipe.','A primeira conversa é gratuita e leva cerca de 30 minutos.','Se o orçamento for limitado, pergunte sobre o programa Built for Impact.'],explore:'Ainda não quer entrar em contato?',browseSectors:'Explore os roteiros por setor →',readApproach:'Leia como a EdZola aborda o trabalho →',required:['seu nome','o nome da sua organização','seu e-mail de trabalho','o tipo de ajuda que procura','o que está dificultando o trabalho hoje'],complete:'Preencha ',validEmail:'Informe um e-mail de trabalho válido.',sending:'Enviando…',captcha:'Conclua a verificação de segurança e tente novamente.',thanks:'Obrigado. Recebemos sua mensagem.',failed:'Não foi possível enviar o formulário agora. Tente novamente em instantes.',contact:'Falar com a EdZola'}
  };
  var ui=translations[locale];
  var slug=(parts[0]||'home');
  var contextKey=path.indexOf('/crm/amplify/')===0?'amplify':(path.indexOf('/team/impactos/')===0?'impactos':(path==='/zolabs/why/'?'why':slug));
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
    'amplify':{
      title:'Apply for the Amplify cohort.',
      body:'Tell us who will join and what you want your Zoho CRM or Bigin account to help your team do. Your application goes straight to EdZola’s CRM.'
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
    },
    'verticals':{
      title:'Bring us the workflow that is creating the most pressure.',
      body:'We’ll help you decide whether to repair one system, connect several handoffs or sequence organisation-wide digital transformation.'
    }
  };
  if(contextKey==='verticals'&&locale==='es')formContexts.verticals={title:'Trae el flujo de trabajo que genera más presión.',body:'Te ayudaremos a decidir si conviene reparar un sistema, conectar varios traspasos o secuenciar una transformación digital de toda la organización.'};
  if(contextKey==='verticals'&&locale==='pt')formContexts.verticals={title:'Traga o fluxo de trabalho que gera mais pressão.',body:'Ajudaremos a decidir se vale reparar um sistema, conectar várias passagens ou sequenciar uma transformação digital em toda a organização.'};
  var context=formContexts[contextKey]||formContexts.home;
  var isAmplify=contextKey==='amplify';
  var formTitle=isAmplify?'Apply for the Amplify cohort.':ui.formTitle;
  var formNote=isAmplify?'You need a paid Zoho CRM or Bigin account, a paid Claude plan, and about 3 hours a week for 4 weeks.':ui.formNote;
  var submitLabel=isAmplify?'Send my Amplify application':ui.submit;

  function createFormHost(){
    var section=document.createElement('section');
    section.className='crm-embed-section';
    section.setAttribute('aria-labelledby','crm-embed-heading');
    section.innerHTML='<div class="crm-embed-inner"><div class="final"><div><h2 id="crm-embed-heading">'+context.title+'</h2><p>'+context.body+'</p></div><div class="contact" data-crm-webform><div class="alt"><b>'+ui.explore+'</b><a href="/sectors/">'+ui.browseSectors+'</a><a href="/thinking/">'+ui.readApproach+'</a></div></div></div></div>';
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
      kicker.textContent=ui.kicker;
      intro.insertBefore(kicker,intro.firstChild);
    }
    if(!intro.querySelector('.form-points')){
      var points=document.createElement('ul');
      points.className='form-points';
      points.innerHTML='<li>'+ui.points[0]+'</li><li>'+ui.points[1]+'</li><li>'+ui.points[2]+'</li>';
      intro.appendChild(points);
    }
  }

  var alt=contact.querySelector('.crm-alt,.alt');
  var altHtml=alt?alt.innerHTML:'<b>'+ui.explore+'</b><a href="/sectors/">'+ui.browseSectors+'</a><a href="/thinking/">'+ui.readApproach+'</a>';
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
    'amplify':'we use Zoho CRM or Bigin and want it to help with donor follow-ups, pipeline reviews or reporting. The people joining will be...',
    'thinking':'one of our programme processes is not working as clearly as it should.',
    'why':'technology is adding work for our team instead of helping them make better decisions.',
    'field-guides':'a tool or workflow was introduced, but the team is struggling to use it consistently.',
    'verticals':'programme, funding, people or operations data is split across tools, and we need to know what to fix first.',
    'contact':'our team spends too much time reconciling trackers and still cannot see what needs attention.'
  };
  if(contextKey==='verticals'&&locale==='es')examples.verticals='los datos de programas, financiación, personas u operaciones están repartidos entre varias herramientas y necesitamos saber qué corregir primero.';
  if(contextKey==='verticals'&&locale==='pt')examples.verticals='os dados de programas, captação, pessoas ou operações estão espalhados por várias ferramentas e precisamos saber o que corrigir primeiro.';

  contact.classList.add('contact','crm-contact');
  contact.id='contact-form';
  contact.innerHTML=''
    +'<h3 class="form-title">'+formTitle+'</h3>'
    +'<p class="form-note">'+formNote+'</p>'
    +'<div id="crmWebToEntityForm" class="zcwf_lblLeft crmWebToEntityForm">'
    +'<div class="wf_customMessageBox" id="wf_splash" style="display:none"><div class="wf_customCircle"><div class="wf_customCheckMark"></div></div><span id="wf_splash_info"></span></div>'
    +'<form id="webform4805054000017631043" name="WebToLeads4805054000017631043" accept-charset="UTF-8" novalidate>'
    +'<input type="hidden" name="xnQsjsdp" value="1aade6b3cf8605c22d9acb6ee15fe0c428d2691bb6cf81fb9b3d225fdc32db68">'
    +'<input type="hidden" name="zc_gad" id="zc_gad" value="">'
    +'<input type="hidden" name="xmIwtLD" value="3b79072affb4a67d4ba6bb28b81a6a3d0aa0725f4c8cad64a6070747b18b1cb86d26b59432bd3601ee65f8da8a548744">'
    +'<input type="hidden" name="actionType" value="TGVhZHM=">'
    +'<input type="hidden" name="returnURL" value="null">'
    +'<!-- Do not remove this code. -->'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Last_Name">'+ui.name+' <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="text" id="Last_Name" aria-required="true" name="Last Name" maxlength="80" autocomplete="name" placeholder="'+ui.namePlaceholder+'"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Company">'+ui.organisation+' <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="text" id="Company" aria-required="true" name="Company" maxlength="200" autocomplete="organization" placeholder="'+ui.organisationPlaceholder+'"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="Email">'+ui.email+' <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><input type="email" ftype="email" id="Email" aria-required="true" name="Email" maxlength="100" autocomplete="email" placeholder="you@yourorganisation.org"></div></div>'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="LEADCF41">'+ui.help+' <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><select class="zcwf_col_fld_slt" id="LEADCF41" aria-required="true" name="LEADCF41"><option value="-None-">'+ui.choose+'</option><option value="Data Systems – MIS / ERP">'+ui.programme+'</option><option value="CRM">'+ui.relationships+'</option><option value="HRMS">'+ui.people+'</option><option value="zolabs.ai – Qualitative Data Collection">'+ui.research+'</option><option value="zolashield – DPDP Compliance">'+ui.protection+'</option><option value="Custom AI Solutions">'+ui.customAi+'</option><option value="AI Workshops and Advisory">'+ui.aiAdvice+'</option><option value="Built for Impact program">'+ui.builtForImpact+'</option></select></div></div>'
    +'<input type="hidden" id="LEADCF121" name="LEADCF121" value="">'
    +'<div class="zcwf_row"><div class="zcwf_col_lab"><label for="LEADCF40">'+ui.barrier+' <span class="required" aria-hidden="true">*</span></label></div><div class="zcwf_col_fld"><textarea id="LEADCF40" aria-required="true" name="LEADCF40" placeholder="'+ui.example+(examples[contextKey]||examples.contact)+'"></textarea></div></div>'
    +'<input type="hidden" name="aG9uZXlwb3Q" value="" tabindex="-1" autocomplete="off">'
    +'<div class="form-actions"><input type="submit" id="formsubmit" class="formsubmit zcwf_button" value="'+submitLabel+'" aria-label="'+submitLabel+'"><input type="reset" class="zcwf_button formreset" value="'+ui.clear+'" aria-label="'+ui.clearForm+'"></div>'
    +'<p class="privacy-note">'+ui.privacy+'</p><p class="form-status" id="crm-form-status" role="status" aria-live="polite"></p>'
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
    'fundzola':'Data Systems – MIS / ERP',
    'amplify':'CRM',
    'verticals':'Data Systems – MIS / ERP'
  };
  if(helpDefaults[contextKey])helpField.value=helpDefaults[contextKey];
  var preserveStatus=false;

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
    var labels=ui.required;
    for(var i=0;i<fields.length;i++){
      var field=form.elements[fields[i]];
      if(!field||!String(field.value).trim()||(field.tagName==='SELECT'&&field.value==='-None-')){
        showStatus(ui.complete+labels[i]+'.',true);
        if(field)field.focus();
        return false;
      }
    }
    if(!validEmail(form.elements.Email)){
      showStatus(ui.validEmail,true);
      form.elements.Email.focus();
      return false;
    }
    return true;
  }

  form.addEventListener('reset',function(){
    var keepStatus=preserveStatus;
    window.setTimeout(function(){
      landingField.value=landingUrl;
      helpField.value=helpDefaults[contextKey]||'-None-';
      if(!keepStatus)showStatus('',false);
    },0);
  });
  form.addEventListener('submit',function(event){
    event.preventDefault();
    showStatus('',false);
    landingField.value=landingUrl;
    if(!mandatoryFieldsPresent())return;
    if(typeof _wfa_track!=='undefined'&&_wfa_track.wfa_submit)_wfa_track.wfa_submit(event);
    var button=form.querySelector('.formsubmit');
    button.disabled=true;
    button.value=ui.sending;
    fetch('https://crm.zoho.com/crm/WebToLeadForm',{method:'POST',body:new FormData(form),cache:'no-cache'})
      .then(function(response){var type=response.headers.get('Content-Type')||'';return type.indexOf('application/json')>-1?response.json():response.text()})
      .then(function(data){
        if(typeof data==='object'&&data.invalidCaptcha==='true'){
          showStatus(data.actionvalue||ui.captcha,true);
          return;
        }
        if(typeof data==='object'&&data.redirectUrl){window.location.assign(data.redirectUrl);return;}
        if(typeof data==='object'&&data.message&&data.actionsubmit==='error_msg'){
          showStatus(data.message,true);
          return;
        }
        var message=document.getElementById('wf_splash_info');
        var splash=document.getElementById('wf_splash');
        var confirmation=typeof data==='object'&&data.actionvalue?data.actionvalue:ui.thanks;
        message.textContent=confirmation;
        splash.style.display='flex';
        preserveStatus=true;
        HTMLFormElement.prototype.reset.call(form);
        preserveStatus=false;
        showStatus(confirmation,false);
        window.setTimeout(function(){splash.style.display='none'},5000);
        if(typeof _wfa_track!=='undefined'&&_wfa_track.wfa_post_submit)_wfa_track.wfa_post_submit(event);
      })
      .catch(function(){showStatus(ui.failed,true)})
      .finally(function(){button.disabled=false;button.value=submitLabel});
  });

  if(typeof _wfa_fstprtcken==='undefined')window._wfa_fstprtcken={};
  window._wfa_fstprtcken[4805054000017631043]=true;

  document.querySelectorAll('a[href^="mailto:reachus@edzola.com"],a[href^="/contact/"]').forEach(function(link){
    link.href='#contact-form';
    if(link.textContent.trim()==='reachus@edzola.com')link.textContent=ui.contact;
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
