// Single source of truth for the shared edzola.ai header, mobile navigation and footer.
// Rendered into every public page by scripts/build-site-shell.mjs. Edit navigation here,
// then run `node scripts/build-site-shell.mjs` — never edit the generated markup in pages.

const esc = (value) => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const LOCALES = ['en', 'es', 'pt'];
const LOCALISED_ROUTES = new Set();

// Routes with a translated page, e.g. "/about/" -> /es/about/ and /pt/about/.
export function registerLocalisedRoutes(files) {
  for (const file of files) {
    const match = file.match(/^(es|pt)\/(.*)index\.html$/);
    if (match) LOCALISED_ROUTES.add('/' + match[2]);
  }
}

function localise(href, locale) {
  if (locale === 'en' || !href.startsWith('/')) return href;
  const [path, hash = ''] = href.split('#');
  if (!LOCALISED_ROUTES.has(path)) return href;
  return `/${locale}${path}${hash ? '#' + hash : ''}`;
}

const T = {
  en: {
    home: 'EdZola home', primary: 'Primary navigation', solutions: 'Solutions', sectors: 'Sectors', work: 'Work', resources: 'Resources', company: 'Company',
    talk: 'Talk to us', menu: 'Menu', close: 'Close', language: 'Change language', languageLabel: 'Language', current: 'Current language', other: 'Read in English',
    sol: { kicker: 'Start with the pressure point', title: 'What needs to work better?', body: 'Choose the part of the organisation slowing people down. Find the right first step before choosing software.', all: 'See all solutions →', core: 'Core systems', ai: 'AI in real work', access: 'Access & funding' },
    sec: { kicker: 'Built for context', title: 'Find the programme model closest to yours.', body: 'Explore the decisions, workflows and evidence that change across social-impact work.', all: 'Browse all 16 sector playbooks →', people: 'People, care & rights', place: 'Communities, planet & culture' },
    wrk: { kicker: 'Work and outcomes', title: 'See what changed after the system went live.', body: 'Explore the problem, the people using the system and the evidence behind the result.', all: 'Visit the Work hub →', cases: 'Case studies', need: 'Explore by need' },
    res: { kicker: 'Useful before a sales call', title: 'Read, compare and plan.', body: 'Practical material from six years of building with the impact sector.', learn: 'Learn and compare', think: 'Tools and thinking' },
    co: { kicker: 'EdZola', title: 'Part technologists. Part sector practitioners.', body: 'Headquartered in Coimbatore, working with impact organisations across five countries.', meet: 'Meet EdZola', touch: 'Get in touch' },
    foot: { tagline: 'Systems built for the world’s hardest work.', place: 'EdZola Technologies · Coimbatore, India', explore: 'Explore', learn: 'Learn', edzola: 'EdZola', rights: 'EdZola Technologies Private Limited', privacy: 'Privacy policy', terms: 'Terms of use', social: 'EdZola on social media' },
  },
  es: {
    home: 'Inicio de EdZola', primary: 'Navegación principal', solutions: 'Soluciones', sectors: 'Sectores', work: 'Trabajo', resources: 'Recursos', company: 'EdZola',
    talk: 'Hablemos', menu: 'Menú', close: 'Cerrar', language: 'Cambiar idioma', languageLabel: 'Idioma', current: 'Idioma actual', other: 'Leer en español',
    sol: { kicker: 'Empieza por el punto de presión', title: '¿Qué necesita funcionar mejor?', body: 'Elige la parte de la organización que está frenando al equipo. Encuentra el primer paso correcto antes de elegir software.', all: 'Ver todas las soluciones →', core: 'Sistemas centrales', ai: 'IA en el trabajo real', access: 'Acceso y financiación' },
    sec: { kicker: 'Hecho para cada contexto', title: 'Encuentra el modelo de programa más cercano al tuyo.', body: 'Explora las decisiones, flujos y evidencias que cambian en cada tipo de trabajo social.', all: 'Ver los 16 itinerarios por sector →', people: 'Personas, cuidado y derechos', place: 'Comunidades, planeta y cultura' },
    wrk: { kicker: 'Trabajo y resultados', title: 'Mira qué cambió cuando el sistema entró en uso.', body: 'Explora el problema, las personas que usan el sistema y la evidencia detrás del resultado.', all: 'Ver todo el trabajo →', cases: 'Casos de estudio', need: 'Explorar por necesidad' },
    res: { kicker: 'Útil antes de hablar', title: 'Lee, compara y planifica.', body: 'Material práctico de seis años construyendo con el sector social.', learn: 'Aprender y comparar', think: 'Herramientas e ideas' },
    co: { kicker: 'EdZola', title: 'Parte tecnólogos. Parte practicantes del sector.', body: 'Con sede en Coimbatore, trabajando con organizaciones de impacto en cinco países.', meet: 'Conoce EdZola', touch: 'Contacto' },
    foot: { tagline: 'Sistemas hechos para el trabajo más difícil del mundo.', place: 'EdZola Technologies · Coimbatore, India', explore: 'Explorar', learn: 'Aprender', edzola: 'EdZola', rights: 'EdZola Technologies Private Limited', privacy: 'Política de privacidad', terms: 'Términos de uso', social: 'EdZola en redes sociales' },
  },
  pt: {
    home: 'Página inicial da EdZola', primary: 'Navegação principal', solutions: 'Soluções', sectors: 'Setores', work: 'Trabalho', resources: 'Recursos', company: 'EdZola',
    talk: 'Fale conosco', menu: 'Menu', close: 'Fechar', language: 'Mudar idioma', languageLabel: 'Idioma', current: 'Idioma atual', other: 'Ler em português',
    sol: { kicker: 'Comece pelo ponto de pressão', title: 'O que precisa funcionar melhor?', body: 'Escolha a parte da organização que está travando a equipe. Encontre o primeiro passo certo antes de escolher software.', all: 'Ver todas as soluções →', core: 'Sistemas centrais', ai: 'IA no trabalho real', access: 'Acesso e financiamento' },
    sec: { kicker: 'Feito para cada contexto', title: 'Encontre o modelo de programa mais próximo do seu.', body: 'Explore as decisões, fluxos e evidências que mudam em cada tipo de trabalho social.', all: 'Ver os 16 roteiros por setor →', people: 'Pessoas, cuidado e direitos', place: 'Comunidades, planeta e cultura' },
    wrk: { kicker: 'Trabalho e resultados', title: 'Veja o que mudou quando o sistema entrou em uso.', body: 'Explore o problema, as pessoas que usam o sistema e a evidência por trás do resultado.', all: 'Ver todo o trabalho →', cases: 'Estudos de caso', need: 'Explorar por necessidade' },
    res: { kicker: 'Útil antes de conversar', title: 'Leia, compare e planeje.', body: 'Material prático de seis anos construindo com o setor social.', learn: 'Aprender e comparar', think: 'Ferramentas e reflexões' },
    co: { kicker: 'EdZola', title: 'Parte tecnólogos. Parte praticantes do setor.', body: 'Sediada em Coimbatore, trabalhando com organizações de impacto em cinco países.', meet: 'Conheça a EdZola', touch: 'Contato' },
    foot: { tagline: 'Sistemas feitos para o trabalho mais difícil do mundo.', place: 'EdZola Technologies · Coimbatore, Índia', explore: 'Explorar', learn: 'Aprender', edzola: 'EdZola', rights: 'EdZola Technologies Private Limited', privacy: 'Política de privacidade', terms: 'Termos de uso', social: 'EdZola nas redes sociais' },
  },
};

// [href, en title, en description, es title, es description, pt title, pt description]
const L = (href, ...text) => ({ href, text });
const pick = (item, locale) => {
  const i = LOCALES.indexOf(locale) * 2;
  return { href: item.href, title: item.text[i] ?? item.text[0], desc: item.text[i + 1] ?? item.text[1] };
};

const CORE = [
  L('/verticals/programme-evidence-systems/', 'Programme & evidence', 'MIS, cases, monitoring and reporting', 'Programas y evidencia', 'MIS, casos, monitoreo e informes', 'Programas e evidências', 'MIS, casos, monitoramento e relatórios'),
  L('/verticals/fundraising-donor-grant-systems/', 'Fundraising & grants', 'Donors, pipelines, grants and compliance', 'Financiación y donantes', 'Donantes, oportunidades, subvenciones y cumplimiento', 'Captação e doadores', 'Doadores, oportunidades, subsídios e conformidade'),
  L('/verticals/people-hr-systems/', 'People & HR', 'Teams, attendance, leave and payroll', 'Personas y RR. HH.', 'Equipos, asistencia, permisos y nómina', 'Pessoas e RH', 'Equipes, presença, férias e folha'),
  L('/verticals/finance-operations-systems/', 'Finance & operations', 'Approvals, vendors, assets and workflows', 'Finanzas y operaciones', 'Aprobaciones, proveedores, activos y flujos', 'Finanças e operações', 'Aprovações, fornecedores, ativos e fluxos'),
  L('/verticals/procurement-inventory-systems/', 'Procurement & inventory', 'Purchasing, stock and reconciliation', 'Compras e inventario', 'Compras, existencias y conciliación', 'Compras e estoque', 'Compras, estoque e conciliação'),
];
const AI = [
  L('/zolabs/', 'Zolabs · Listen', 'Voice research and evaluation at scale', 'Zolabs · Escuchar', 'Investigación por voz y evaluación a escala', 'Zolabs · Ouvir', 'Pesquisa por voz e avaliação em escala'),
  L('/zolashield/', 'ZolaShield · Protect', 'DPDP readiness and safer data practices', 'ZolaShield · Proteger', 'Preparación DPDP y datos más seguros', 'ZolaShield · Proteger', 'Preparação DPDP e dados mais seguros'),
  L('/dozai/', 'DozAI · Run', 'AI agents for high-volume nonprofit workflows', 'DozAI · Operar', 'Agentes de IA para flujos de alto volumen', 'DozAI · Operar', 'Agentes de IA para fluxos de alto volume'),
];
const SECTORS_PEOPLE = [
  L('/education/', 'Education', 'Learner journeys', 'Educación', 'Trayectorias de aprendizaje', 'Educação', 'Trajetórias de aprendizagem'),
  L('/youth-employability/', 'Youth & employability', 'Skills to sustained work', 'Juventud y empleo', 'De la formación al empleo', 'Juventude e emprego', 'Da formação ao emprego'),
  L('/health/', 'Health & wellbeing', 'Care and follow-up', 'Salud y bienestar', 'Atención y seguimiento', 'Saúde e bem-estar', 'Cuidado e acompanhamento'),
  L('/maternal-child-health/', 'Maternal & child health', 'Pregnancy to early childhood', 'Salud materno-infantil', 'Del embarazo a la primera infancia', 'Saúde materno-infantil', 'Da gestação à primeira infância'),
  L('/mental-health/', 'Mental health', 'Screening and continuing care', 'Salud mental', 'Detección y atención continua', 'Saúde mental', 'Triagem e cuidado contínuo'),
  L('/child-protection/', 'Child protection', 'Cases and safe transitions', 'Protección infantil', 'Casos y transiciones seguras', 'Proteção infantil', 'Casos e transições seguras'),
  L('/gender/', 'Gender equality', 'Choice, safety and control', 'Igualdad de género', 'Decisión, seguridad y control', 'Igualdade de gênero', 'Escolha, segurança e controle'),
  L('/disability/', 'Disability inclusion', 'Access and participation', 'Inclusión y discapacidad', 'Acceso y participación', 'Inclusão e deficiência', 'Acesso e participação'),
];
const SECTORS_PLACE = [
  L('/livelihoods/', 'Livelihoods', 'Households and enterprises', 'Medios de vida', 'Hogares y emprendimientos', 'Meios de vida', 'Famílias e empreendimentos'),
  L('/environment/', 'Environment & climate', 'Landscapes and adaptation', 'Ambiente y clima', 'Territorios y adaptación', 'Meio ambiente e clima', 'Territórios e adaptação'),
  L('/waste/', 'Waste & circularity', 'Collection and recovery', 'Residuos y circularidad', 'Recolección y recuperación', 'Resíduos e circularidade', 'Coleta e recuperação'),
  L('/food-systems/', 'Food & nutrition', 'Producers and nutrition', 'Alimentación y nutrición', 'Productores y nutrición', 'Alimentação e nutrição', 'Produtores e nutrição'),
  L('/community-development/', 'Community development', 'Plans and participation', 'Desarrollo comunitario', 'Planes y participación', 'Desenvolvimento comunitário', 'Planos e participação'),
  L('/justice/', 'Access to justice', 'Cases, remedies and rights', 'Acceso a la justicia', 'Casos, remedios y derechos', 'Acesso à justiça', 'Casos, reparações e direitos'),
  L('/media/', 'Media & journalism', 'Stories and public change', 'Medios y periodismo', 'Historias y cambio público', 'Mídia e jornalismo', 'Histórias e mudança pública'),
  L('/arts/', 'Arts & culture', 'Artists, grants and audiences', 'Arte y cultura', 'Artistas, becas y públicos', 'Arte e cultura', 'Artistas, editais e públicos'),
];
const CASES = [
  L('https://www.edzola.com/post/compass-mis-transforming-state-wide-teacher-training-with-tech', 'Simple Education Foundation', 'Teacher development across four states', 'Simple Education Foundation', 'Formación docente en cuatro estados', 'Simple Education Foundation', 'Formação docente em quatro estados'),
  L('https://www.edzola.com/post/edg-trust-for-retailers-retail-associates-of-india-streamlining-program-management', 'TRRAIN', 'Operations for 10,000+ trainees a year', 'TRRAIN', 'Operaciones para más de 10.000 participantes al año', 'TRRAIN', 'Operações para mais de 10 mil participantes por ano'),
  L('https://www.edzola.com/post/tap-india-foundation-tracking-out-of-school-children-data-with-zoho-creator', 'TAP India Foundation', '16,000+ out-of-school children tracked', 'TAP India Foundation', 'Más de 16.000 niños fuera de la escuela', 'TAP India Foundation', 'Mais de 16 mil crianças fora da escola'),
  L('https://www.edzola.com/the-nudge-future-perfect', 'The/Nudge Institute', 'Ten tools connected around one journey', 'The/Nudge Institute', 'Diez herramientas conectadas en un recorrido', 'The/Nudge Institute', 'Dez ferramentas conectadas em uma jornada'),
  L('https://www.edzola.com/post/edg-aangan-trust-streamlining-hr-operations-and-employee-data-management-through-zoho-people', 'Aangan Trust', 'One HR system for staff across locations', 'Aangan Trust', 'Un sistema de RR. HH. para todas las sedes', 'Aangan Trust', 'Um sistema de RH para todas as unidades'),
];
const NEEDS = [
  L('/work/#programme', 'Programme systems', 'Delivery, cases, evidence and reporting', 'Sistemas de programas', 'Ejecución, casos, evidencia e informes', 'Sistemas de programas', 'Execução, casos, evidências e relatórios'),
  L('/work/#fundraising', 'Funding systems', 'Donor relationships and grant workflows', 'Sistemas de financiación', 'Relación con donantes y subvenciones', 'Sistemas de captação', 'Relacionamento com doadores e subsídios'),
  L('/work/#operations', 'People & operations', 'Teams, approvals and internal work', 'Personas y operaciones', 'Equipos, aprobaciones y trabajo interno', 'Pessoas e operações', 'Equipes, aprovações e trabalho interno'),
];
const LEARN = [
  L('/learn/', 'Implementation library', 'Guides for choosing and building systems', 'Biblioteca de implementación', 'Guías para elegir y construir sistemas', 'Biblioteca de implementação', 'Guias para escolher e construir sistemas'),
  L('/solutions/', 'Solution guides', 'MIS, CRM, M&E, AI agents and more', 'Guías de soluciones', 'MIS, CRM, M&E, agentes de IA y más', 'Guias de soluções', 'MIS, CRM, M&A, agentes de IA e mais'),
  L('/learn/compare/', 'Compare approaches', 'Custom, configured or off the shelf', 'Comparar enfoques', 'A medida, configurado o estándar', 'Comparar abordagens', 'Sob medida, configurado ou pronto'),
  L('/learn/technology/', 'Technology guides', 'Platforms such as Zoho, explained plainly', 'Guías de tecnología', 'Plataformas como Zoho, explicadas con claridad', 'Guias de tecnologia', 'Plataformas como Zoho, explicadas com clareza'),
];
const THINK = [
  L('/resources/', 'Templates & tools', 'Estimators, roadmaps and requirement templates', 'Plantillas y herramientas', 'Estimadores, hojas de ruta y requisitos', 'Modelos e ferramentas', 'Estimadores, roteiros e requisitos'),
  L('/impact-os/', 'ImpactOS', 'The method behind every EdZola project', 'ImpactOS', 'El método detrás de cada proyecto', 'ImpactOS', 'O método por trás de cada projeto'),
  L('/thinking/', 'Thinking & field guides', 'Beliefs, lessons and sector understanding', 'Ideas y guías de campo', 'Convicciones, lecciones y contexto del sector', 'Reflexões e guias de campo', 'Convicções, lições e contexto do setor'),
];
const MEET = [
  L('/about/', 'About & team', 'Who we are and what we have learnt', 'Nosotros y equipo', 'Quiénes somos y qué hemos aprendido', 'Sobre e equipe', 'Quem somos e o que aprendemos'),
  L('/news/', 'News & media', 'Updates, coverage and announcements', 'Noticias y medios', 'Novedades, prensa y anuncios', 'Notícias e imprensa', 'Novidades, imprensa e anúncios'),
  L('https://go.edzola.com/hiring', 'Careers', 'Join the team in Coimbatore', 'Empleo', 'Únete al equipo en Coimbatore', 'Carreiras', 'Junte-se à equipe em Coimbatore'),
];
const TOUCH = [
  L('/contact/', 'Start a conversation', 'Bring us one messy workflow', 'Iniciar una conversación', 'Tráenos un flujo de trabajo complicado', 'Iniciar uma conversa', 'Traga um fluxo de trabalho complicado'),
  L('/patrons/', 'Become a patron', 'Fund systems for nonprofits', 'Hazte mecenas', 'Financia sistemas para organizaciones sociales', 'Torne-se patrono', 'Financie sistemas para organizações sociais'),
  L('https://in.linkedin.com/company/edzola', 'Follow EdZola', 'Updates from the work', 'Sigue a EdZola', 'Novedades del trabajo', 'Siga a EdZola', 'Novidades do trabalho'),
];
const FEATURES = {
  en: [['/patrons/', 'Built for Impact Fund', 'Fund the systems nonprofits need to grow.', 'Back the 2027 cohort →', ''], ['/crm/amplify/', 'Amplify cohort', 'Make Zoho CRM useful in everyday work, with Claude.', 'Apply for the cohort →', ' ez-teal']],
  es: [['/patrons/', 'Fondo Built for Impact', 'Financia los sistemas que las organizaciones necesitan para crecer.', 'Apoya la cohorte 2027 →', ''], ['/crm/amplify/', 'Cohorte Amplify', 'Haz que Zoho CRM sea útil en el día a día, con Claude.', 'Postula a la cohorte →', ' ez-teal']],
  pt: [['/patrons/', 'Fundo Built for Impact', 'Financie os sistemas que as organizações precisam para crescer.', 'Apoie a coorte 2027 →', ''], ['/crm/amplify/', 'Coorte Amplify', 'Torne o Zoho CRM útil no dia a dia, com o Claude.', 'Candidate-se à coorte →', ' ez-teal']],
};
const SOCIAL = [
  ['https://in.linkedin.com/company/edzola', 'LinkedIn', '<path d="M6.5 9.5v8M6.5 6.5v.01M10.5 17.5v-8m0 3.5c0-2 1.2-3.5 3-3.5s3 1.2 3 3.5v4.5"/>'],
  ['https://www.youtube.com/@edzola', 'YouTube', '<rect x="3.5" y="6.5" width="17" height="11" rx="3"/><path d="m10.5 9.5 4 2.5-4 2.5z"/>'],
  ['https://instagram.com/edzolatech', 'Instagram', '<rect x="4.5" y="4.5" width="15" height="15" rx="4.5"/><circle cx="12" cy="12" r="3.5"/><path d="M16.5 7.5v.01"/>'],
  ['https://twitter.com/edzolatech', 'X', '<path d="m5 5 14 14M19 5 5 19"/>'],
];

// Which top-level section a path belongs to, for the "you are here" state.
export function sectionFor(path) {
  const p = path.replace(/^\/(es|pt)(?=\/)/, '');
  if (/^\/(verticals|solutions|zolabs|zolashield|dozai|patrons|crm|fundzola)\//.test(p)) return 'solutions';
  if (p === '/sectors/' || [...SECTORS_PEOPLE, ...SECTORS_PLACE].some((s) => p.startsWith(s.href))) return 'sectors';
  if (/^\/work\//.test(p)) return 'work';
  if (/^\/(learn|resources|impact-os|thinking|field-guides|why)\//.test(p)) return 'resources';
  if (/^\/(about|news|contact)\//.test(p)) return 'company';
  return '';
}

function menuLink(item, locale) {
  const { href, title, desc } = pick(item, locale);
  return `<a class="ez-menu-link" href="${esc(localise(href, locale))}"><b>${esc(title)}</b><small>${esc(desc)}</small></a>`;
}
function sectorLink(item, locale) {
  const { href, title, desc } = pick(item, locale);
  return `<a href="${esc(href)}"><b>${esc(title)}</b><small>${esc(desc)}</small></a>`;
}
function mobileLink(item, locale) {
  const { href, title } = pick(item, locale);
  return `<a href="${esc(localise(href, locale))}">${esc(title)}</a>`;
}
function intro(t, allHref, locale) {
  const all = t.all ? `<a class="ez-menu-all" href="${esc(localise(allHref, locale))}">${esc(t.all)}</a>` : '';
  return `<div class="ez-mega-intro"><span class="ez-kicker">${esc(t.kicker)}</span><p class="ez-mega-title">${esc(t.title)}</p><p>${esc(t.body)}</p>${all}</div>`;
}
const col = (label, inner) => `<div class="ez-menu-col"><span class="ez-menu-label">${esc(label)}</span>${inner}</div>`;

/**
 * @param {object} page
 * @param {'en'|'es'|'pt'} page.locale
 * @param {string} page.path        canonical path, e.g. "/verticals/"
 * @param {{en?:string,es?:string,pt?:string}} page.alternates  reciprocal language routes
 * @param {boolean} [page.staticHeader] render a non-sticky header (pages with their own sticky toolbar)
 */
export function renderHeader({ locale, path, alternates = {}, staticHeader = false }) {
  const t = T[locale];
  const home = locale === 'en' ? '/' : `/${locale}/`;
  const current = sectionFor(path);
  const trigger = (name) => `<button class="ez-nav-trigger${current === name ? ' is-current' : ''}" type="button" data-ez-trigger="${name}" aria-expanded="false" aria-controls="ez-menu-${name}">${esc(t[name])}<svg aria-hidden="true" viewBox="0 0 12 12"><path d="m3 4.5 3 3 3-3"/></svg></button>`;
  const langHref = (code) => alternates[code] || (code === 'en' ? '/' : `/${code}/`);
  const langNames = { en: ['English', 'EN'], es: ['Español', 'ES'], pt: ['Português', 'PT'] };
  const langLinks = LOCALES.map((code) => `<a href="${esc(langHref(code))}" lang="${code}" hreflang="${code}"${code === locale ? ' aria-current="true"' : ''}><b>${langNames[code][0]}</b><small>${code === locale ? esc(t.current) : esc(T[code].other)}</small></a>`).join('');

  const features = FEATURES[locale].map(([href, kicker, strong, cta, tone]) => `<a class="ez-feature${tone}" href="${href}"><span class="ez-kicker">${esc(kicker)}</span><strong>${esc(strong)}</strong><small>${esc(cta)}</small></a>`).join('');

  const megas = [
    ['solutions', 'ez-solutions', intro(t.sol, '/verticals/', locale) + col(t.sol.core, CORE.map((i) => menuLink(i, locale)).join('')) + col(t.sol.ai, AI.map((i) => menuLink(i, locale)).join('')) + col(t.sol.access, features)],
    ['sectors', 'ez-sectors', intro(t.sec, '/sectors/', locale) + col(t.sec.people, `<div class="ez-sector-links">${SECTORS_PEOPLE.map((i) => sectorLink(i, locale)).join('')}</div>`) + col(t.sec.place, `<div class="ez-sector-links">${SECTORS_PLACE.map((i) => sectorLink(i, locale)).join('')}</div>`)],
    ['work', '', intro(t.wrk, '/work/', locale) + col(t.wrk.cases, CASES.map((i) => menuLink(i, locale)).join('')) + col(t.wrk.need, NEEDS.map((i) => menuLink(i, locale)).join(''))],
    ['resources', '', intro(t.res, '', locale) + col(t.res.learn, LEARN.map((i) => menuLink(i, locale)).join('')) + col(t.res.think, THINK.map((i) => menuLink(i, locale)).join(''))],
    ['company', '', intro(t.co, '', locale) + col(t.co.meet, MEET.map((i) => menuLink(i, locale)).join('')) + col(t.co.touch, TOUCH.map((i) => menuLink(i, locale)).join(''))],
  ].map(([name, cls, inner]) => `<div class="ez-mega" id="ez-menu-${name}" data-ez-menu="${name}" hidden><div class="ez-mega-inner ${cls} ez-shell">${inner}</div></div>`).join('');

  const mobileGroup = (name, items, allHref, allLabel, two = false) => `<details${current === name ? ' class="is-current"' : ''}><summary>${esc(t[name])}<span aria-hidden="true"></span></summary><div class="ez-mobile-sub${two ? ' ez-two' : ''}">${items.map((i) => mobileLink(i, locale)).join('')}${allHref ? `<a class="ez-mobile-all" href="${esc(localise(allHref, locale))}">${esc(allLabel)}</a>` : ''}</div></details>`;
  const mobile = `<div class="ez-mobile-nav" id="ez-mobile-nav" data-ez-mobile-nav hidden><div class="ez-mobile-inner">`
    + `<nav class="ez-mobile-language" aria-label="${esc(t.languageLabel)}">${LOCALES.map((code) => `<a href="${esc(langHref(code))}" lang="${code}" hreflang="${code}"${code === locale ? ' aria-current="true"' : ''}>${langNames[code][1]}</a>`).join('')}</nav>`
    + mobileGroup('solutions', [...CORE, ...AI, L('/patrons/', 'Built for Impact Fund', '', 'Fondo Built for Impact', '', 'Fundo Built for Impact', ''), L('/crm/amplify/', 'Amplify cohort', '', 'Cohorte Amplify', '', 'Coorte Amplify', '')], '/verticals/', t.sol.all)
    + mobileGroup('sectors', [...SECTORS_PEOPLE, ...SECTORS_PLACE], '/sectors/', t.sec.all, true)
    + mobileGroup('work', [...NEEDS, ...CASES.slice(0, 4)], '/work/', t.wrk.all)
    + mobileGroup('resources', [...LEARN, ...THINK])
    + mobileGroup('company', [...MEET, ...TOUCH.slice(0, 2)])
    + `<a class="ez-button ez-mobile-cta" href="${esc(localise('/contact/', locale))}">${esc(t.talk)}</a></div></div>`;

  return `<header class="ez-site-shell${staticHeader ? ' ez-static' : ''}" data-ez-header>`
    + `<div class="ez-header-inner ez-shell"><a class="ez-brand" href="${home}" aria-label="${esc(t.home)}">edzola.ai</a>`
    + `<nav class="ez-desktop-nav" aria-label="${esc(t.primary)}">${['solutions', 'sectors', 'work', 'resources', 'company'].map(trigger).join('')}</nav>`
    + `<div class="ez-header-actions"><div class="ez-locale-wrap"><button class="ez-locale-trigger" type="button" data-ez-locale-trigger aria-expanded="false" aria-controls="ez-locale-menu" aria-label="${esc(t.language)}"><svg aria-hidden="true" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.2"/><path d="M1.8 8h12.4M8 1.8c1.7 1.8 2.5 3.8 2.5 6.2S9.7 12.4 8 14.2C6.3 12.4 5.5 10.4 5.5 8S6.3 3.6 8 1.8Z"/></svg>${locale.toUpperCase()}</button>`
    + `<div class="ez-locale-menu" id="ez-locale-menu" data-ez-locale-menu hidden>${langLinks}</div></div>`
    + `<a class="ez-button ez-header-cta" href="${esc(localise('/contact/', locale))}">${esc(t.talk)}</a>`
    + `<button class="ez-mobile-toggle" type="button" data-ez-mobile-toggle aria-expanded="false" aria-controls="ez-mobile-nav"><span class="ez-menu-icon" aria-hidden="true"><i></i><i></i></span><span data-ez-mobile-label data-open="${esc(t.close)}" data-closed="${esc(t.menu)}">${esc(t.menu)}</span></button></div></div>`
    + megas + `</header>` + mobile;
}

export function renderFooter({ locale }) {
  const t = T[locale];
  const f = t.foot;
  const home = locale === 'en' ? '/' : `/${locale}/`;
  const group = (label, items) => `<div class="ez-footer-col"><p class="ez-footer-label">${esc(label)}</p>${items.map((i) => mobileLink(i, locale)).join('')}</div>`;
  const solutions = [L('/verticals/', 'Core systems', '', 'Sistemas centrales', '', 'Sistemas centrais', ''), L('/solutions/', 'Solution guides', '', 'Guías de soluciones', '', 'Guias de soluções', ''), ...AI.map((i) => ({ href: i.href, text: i.text.map((x, n) => (n % 2 === 0 ? x.split(' · ')[0] : x)) })), L('/crm/amplify/', 'Amplify CRM cohort', '', 'Cohorte Amplify', '', 'Coorte Amplify', '')];
  const explore = [L('/sectors/', 'Sectors', '', 'Sectores', '', 'Setores', ''), L('/work/', 'Work & case studies', '', 'Trabajo y casos', '', 'Trabalho e casos', ''), L('/impact-os/', 'ImpactOS', '', 'ImpactOS', '', 'ImpactOS', ''), L('/why/', 'Founding thesis', '', 'Tesis fundacional', '', 'Tese fundadora', '')];
  const learn = [LEARN[0], THINK[0], L('/thinking/', 'Thinking', '', 'Ideas', '', 'Reflexões', ''), L('/field-guides/technology-that-sticks/', 'Field guides', '', 'Guías de campo', '', 'Guias de campo', '')];
  const company = [L('/about/', 'About & team', '', 'Nosotros y equipo', '', 'Sobre e equipe', ''), MEET[1], MEET[2], L('/patrons/', 'Become a patron', '', 'Hazte mecenas', '', 'Torne-se patrono', ''), L('/contact/', 'Contact', '', 'Contacto', '', 'Contato', '')];
  const social = SOCIAL.map(([href, name, icon]) => `<a href="${href}" rel="noopener" aria-label="EdZola on ${name}"><svg aria-hidden="true" viewBox="0 0 24 24">${icon}</svg></a>`).join('');
  return `<footer class="ez-footer"><div class="ez-shell"><div class="ez-footer-grid">`
    + `<div class="ez-footer-brand"><a class="ez-brand" href="${home}">edzola.ai</a><p>${esc(f.tagline)}<br>${esc(f.place)}</p><p><a href="mailto:reachus@edzola.com">reachus@edzola.com</a></p><nav class="ez-social" aria-label="${esc(f.social)}">${social}</nav></div>`
    + group(t.solutions, solutions) + group(f.explore, explore) + group(f.learn, learn) + group(f.edzola, company)
    + `</div><div class="ez-footer-bottom"><span>© ${new Date().getFullYear()} ${esc(f.rights)}</span><span><a href="https://www.edzola.com/privacy-policy-edzola">${esc(f.privacy)}</a><a href="https://www.edzola.com/terms-of-use">${esc(f.terms)}</a></span></div></div></footer>`;
}

