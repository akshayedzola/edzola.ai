"""Build Spanish and Portuguese copies of selected pages.

  python3 scripts/i18n/i18n.py extract   # list every translatable string in the English pages
  python3 scripts/i18n/i18n.py build     # write /es/ and /pt/ pages from es.json and pt.json

Strings are matched exactly; anything missing from a language file stays in English
and is reported, so editing an English page and re-running "extract" shows what to translate.
Markup inside a string is reduced to numbered placeholders (<1>…</1>, <2/>) which the
translation must keep.
"""
import json, re, sys, os, copy
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {'index.html': '', 'about/index.html': 'about/', 'impact-os/index.html': 'impact-os/', 'zolabs/index.html': 'zolabs/'}
LANGS = {'es': {'html': 'es', 'og': 'es_419', 'name': 'Español'}, 'pt': {'html': 'pt-BR', 'og': 'pt_BR', 'name': 'Português'}}
INLINE = {'a', 'b', 'strong', 'em', 'i', 'span', 'small', 'br', 'sup', 'sub', 'code', 'abbr', 'u', 'mark', 'cite', 'img', 'svg', 'time', 'q', 's'}
SKIP = {'script', 'style', 'noscript', 'svg', 'template', 'canvas'}
ATTRS = ('alt', 'aria-label', 'title', 'placeholder')
META = ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description')
HAS_WORDS = re.compile(r'[A-Za-z]{2,}')
# Strings drawn by the homepage hero animation (canvas text and captions).
JS_KEYS_FILE = os.path.join(HERE, 'js_strings.json')


def inline_tree(el):
    return all(d.name in INLINE for d in el.descendants if isinstance(d, Tag))


def own_text(el):
    return any(isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() for c in el.children)


def blocks(soup):
    out = []
    def walk(el):
        for c in el.children:
            if not isinstance(c, Tag) or c.name in SKIP:
                continue
            if c.get('data-i18n') == 'skip' or c.get('aria-hidden') == 'true' and c.name == 'span' and 'dup' in (c.get('class') or []):
                continue
            if inline_tree(c) and c.get_text(strip=True):
                kids = [k for k in c.children if isinstance(k, Tag) and k.get_text(strip=True)]
                if not own_text(c) and len(kids) > 1:
                    walk(c)
                else:
                    out.append(c)
            else:
                walk(c)
    walk(soup.body)
    return out


def encode(el):
    """Inner HTML with tags replaced by numbered placeholders; returns (key, tags)."""
    tags, parts = [], []
    def rec(node):
        for c in node.children:
            if isinstance(c, Comment):
                continue
            if isinstance(c, NavigableString):
                parts.append(re.sub(r'\s+', ' ', str(c)).replace('<', '&lt;'))
            elif c.name in ('br', 'img', 'svg') or not c.get_text(strip=True) and c.name != 'a':
                tags.append(c); parts.append(f'<{len(tags)}/>')
            else:
                tags.append(c); n = len(tags); parts.append(f'<{n}>'); rec(c); parts.append(f'</{n}>')
    rec(el)
    return ''.join(parts).strip(), tags


def decode(el, translation, tags, soup):
    el.clear()
    pos = 0
    stack = [el]
    for m in re.finditer(r'<(/?)(\d+)(/?)>', translation):
        text = translation[pos:m.start()]
        if text:
            stack[-1].append(NavigableString(text.replace('&lt;', '<')))
        n = int(m.group(2)) - 1
        if m.group(3):
            stack[-1].append(copy.copy(tags[n]))
        elif not m.group(1):
            shell = copy.copy(tags[n]); shell.clear(); stack[-1].append(shell); stack.append(shell)
        else:
            stack.pop()
        pos = m.end()
    if translation[pos:]:
        stack[-1].append(NavigableString(translation[pos:].replace('&lt;', '<')))


def collect(path):
    soup = BeautifulSoup(open(os.path.join(ROOT, path), encoding='utf-8').read(), 'html.parser')
    keys = []
    if soup.title and soup.title.string:
        keys.append(soup.title.string.strip())
    for m in soup.find_all('meta'):
        if (m.get('name') or m.get('property')) in META and m.get('content'):
            keys.append(m['content'])
    for el in blocks(soup):
        k, _ = encode(el)
        if HAS_WORDS.search(k):
            keys.append(k)
    for el in soup.body.find_all(True):
        for a in ATTRS:
            if el.get(a) and HAS_WORDS.search(el[a]) and not el.find_parent(SKIP - {'svg'}):
                keys.append(el[a])
    return keys


def extract():
    seen, order = set(), []
    for p in PAGES:
        for k in collect(p):
            if k not in seen:
                seen.add(k); order.append(k)
    if os.path.exists(JS_KEYS_FILE):
        for k in json.load(open(JS_KEYS_FILE)):
            if k not in seen:
                seen.add(k); order.append(k)
    for lang in LANGS:
        f = os.path.join(HERE, f'{lang}.json')
        have = json.load(open(f)) if os.path.exists(f) else {}
        missing = [k for k in order if k not in have]
        print(f'{lang}: {len(order)} strings, {len(missing)} untranslated')
    json.dump(order, open(os.path.join(HERE, 'strings.json'), 'w'), ensure_ascii=False, indent=0)


def localise_href(href, lang):
    for prefix in ('https://edzola.ai', ''):
        for src, dst in PAGES.items():
            u = prefix + '/' + dst
            if href == u or href.startswith(u + '#') and dst == '':
                return f'/{lang}/{dst}' + href[len(u):]
            if dst and href.startswith(u):
                return f'/{lang}/{dst}' + href[len(u):]
    return href


def alternates(dst):
    tags = [f'<link rel="alternate" hreflang="en" href="https://edzola.ai/{dst}">']
    for l, c in LANGS.items():
        tags.append(f'<link rel="alternate" hreflang="{c["html"]}" href="https://edzola.ai/{l}/{dst}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="https://edzola.ai/{dst}">')
    return '\n'.join(tags)


def switcher(dst, current, labels):
    links = [('en', f'/{dst}', 'EN')] + [(l, f'/{l}/{dst}', l.upper()) for l in LANGS]
    a = ''.join(f'<a href="{h}" hreflang="{l}" lang="{l}"{" aria-current=\"true\"" if l == current else ""}>{t}</a>' for l, h, t in links)
    return f'<div class="gh-lang" data-i18n="skip" role="navigation" aria-label="{labels}">{a}</div>'


LANG_CSS = '''<style id="gh-lang-css">
.gh-lang{display:flex;gap:2px;padding:3px;border:1px solid #EADFD6;border-radius:999px;background:#fff;font:600 12px/1 "JetBrains Mono","IBM Plex Mono",ui-monospace,monospace}
.gh-lang a{padding:6px 8px;border-radius:999px;color:#6B6360!important}
.gh-lang a[aria-current]{background:#1A1A1A;color:#FDF8F4!important}
.gh-lang a:hover{color:#1A1A1A!important}
.gh-drop .gh-lang{margin:8px 6px 4px;justify-content:center}
@media (max-width:900px){.gh-in>.gh-lang{display:none}}
.lang-hint{position:fixed;left:16px;right:16px;bottom:16px;z-index:70;max-width:440px;margin-left:auto;display:flex;align-items:center;gap:12px;padding:14px 16px;background:#1A1A1A;color:#FDF8F4;border-radius:16px;box-shadow:0 18px 40px rgba(0,0,0,.25);font:500 14px/1.4 "Figtree",system-ui,sans-serif}
.lang-hint a{color:#1A1A1A;background:#E8967A;padding:8px 14px;border-radius:999px;font-weight:700;text-decoration:none;white-space:nowrap}
.lang-hint button{margin-left:auto;background:none;border:0;color:#FDF8F4;opacity:.7;font-size:20px;cursor:pointer;padding:4px 6px}
</style>'''

HINT_JS = '''<script id="lang-hint">
(function(){
  var dst=%s, offers={es:['¿Prefieres leer en español?','Ver en español'],pt:['Prefere ler em português?','Ver em português']};
  function get(){try{return localStorage.getItem('edz-lang')}catch(e){return null}}
  function set(v){try{localStorage.setItem('edz-lang',v)}catch(e){}}
  document.querySelectorAll('.gh-lang a').forEach(function(a){a.addEventListener('click',function(){set(a.getAttribute('hreflang'))})});
  if(document.documentElement.lang.slice(0,2)!=='en'||get())return;
  var pref=(navigator.languages||[navigator.language||''])[0].slice(0,2).toLowerCase();
  if(!offers[pref]){
    /* No es/pt browser language: fall back to the device time zone, which stays on the device. */
    var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
    var PT=/^(America\\/(Sao_Paulo|Bahia|Fortaleza|Recife|Belem|Manaus|Cuiaba|Campo_Grande|Porto_Velho|Boa_Vista|Rio_Branco|Araguaina|Maceio|Santarem|Noronha|Eirunepe)|Europe\\/Lisbon|Atlantic\\/(Azores|Madeira|Cape_Verde)|Africa\\/(Maputo|Luanda|Bissau|Sao_Tome))$/;
    var ES=/^(America\\/(Argentina\\/.*|Buenos_Aires|Mexico_City|Cancun|Merida|Monterrey|Matamoros|Chihuahua|Ciudad_Juarez|Ojinaga|Mazatlan|Bahia_Banderas|Hermosillo|Tijuana|Bogota|Lima|Santiago|Punta_Arenas|Caracas|Guayaquil|La_Paz|Asuncion|Montevideo|Guatemala|El_Salvador|Tegucigalpa|Managua|Costa_Rica|Panama|Havana|Santo_Domingo|Puerto_Rico)|Europe\\/Madrid|Africa\\/(Ceuta|Malabo)|Atlantic\\/Canary|Pacific\\/(Galapagos|Easter))$/;
    pref=PT.test(tz)?'pt':ES.test(tz)?'es':'';
  }
  if(!offers[pref])return;
  var d=document.createElement('div');d.className='lang-hint';d.setAttribute('role','region');d.setAttribute('aria-label','Language');
  d.innerHTML='<span lang="'+pref+'">'+offers[pref][0]+'</span><a lang="'+pref+'" href="/'+pref+'/'+dst+'">'+offers[pref][1]+'</a><button aria-label="Dismiss">×</button>';
  d.querySelector('a').addEventListener('click',function(){set(pref)});
  d.querySelector('button').addEventListener('click',function(){set('en');d.remove()});
  document.body.appendChild(d);
})();
</script>'''


def strip_lang_ui(html):
    html = re.sub(r'<div class="gh-lang"[^>]*>.*?</div>', '', html)
    html = re.sub(r'<style id="gh-lang-css">.*?</style>\n?', '', html, flags=re.S)
    html = re.sub(r'<link rel="alternate" hreflang[^>]*>\n?', '', html)
    html = re.sub(r'<script id="lang-hint">.*?</script>\n?', '', html, flags=re.S)
    return html


def add_lang_ui(html, dst, current, label):
    sw = switcher(dst, current, label)
    html = re.sub(r'(<a [^>]*class="gh-cta")', lambda m: sw + m.group(1), html, count=1)
    html = re.sub(r'(<div [^>]*class="gh-drop"[^>]*>)', lambda m: m.group(1) + sw, html, count=1)
    html = html.replace('</head>', LANG_CSS + '\n' + alternates(dst) + '\n</head>', 1)
    html = html.replace('</body>', HINT_JS % json.dumps(dst) + '\n</body>', 1)
    return html


def build():
    js_keys = json.load(open(JS_KEYS_FILE)) if os.path.exists(JS_KEYS_FILE) else []
    report = {}
    for lang, conf in LANGS.items():
        tr = json.load(open(os.path.join(HERE, f'{lang}.json')))
        missing = set()
        for src, dst in PAGES.items():
            raw = strip_lang_ui(open(os.path.join(ROOT, src), encoding='utf-8').read())
            soup = BeautifulSoup(raw, 'html.parser')
            T = lambda k: tr.get(k) or (missing.add(k) or k)
            if soup.title and soup.title.string:
                soup.title.string = T(soup.title.string.strip())
            for m in soup.find_all('meta'):
                key = m.get('name') or m.get('property')
                if key in META and m.get('content'):
                    m['content'] = T(m['content'])
                if key == 'og:url':
                    m['content'] = f'https://edzola.ai/{lang}/{dst}'
            for el in blocks(soup):
                k, tags = encode(el)
                if HAS_WORDS.search(k):
                    t = T(k)
                    if t != k:
                        decode(el, t, tags, soup)
            for el in soup.body.find_all(True):
                for a in ATTRS:
                    if el.get(a) and HAS_WORDS.search(el[a]) and el[a] in tr:
                        el[a] = tr[el[a]]
                if el.name == 'a' and el.get('href'):
                    el['href'] = localise_href(el['href'], lang)
            if lang == 'pt':  # Brazilian digit grouping: 10,000 -> 10.000
                for t in soup.body.find_all(string=re.compile(r'\d,\d{3}')):
                    if not t.find_parent(['script', 'style']):
                        t.replace_with(re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '.', str(t)))
            for l in soup.find_all('link', rel='canonical'):
                l['href'] = f'https://edzola.ai/{lang}/{dst}'
            soup.html['lang'] = conf['html']
            og = soup.find('meta', property='og:type')
            if og:
                loc = soup.new_tag('meta', property='og:locale'); loc['content'] = conf['og']; og.insert_after(loc)
            html = str(soup)
            # JSON-LD and script strings: exact string replacement of known keys
            def sub_scripts(m):
                body = m.group(2)
                for k in sorted(set(js_keys) | {x for x in tr if len(x) > 12}, key=len, reverse=True):
                    if k not in tr or k not in body:
                        continue
                    for q in ('"', "'", '`'):
                        esc = json.dumps(k, ensure_ascii=False)[1:-1] if q == '"' else k
                        val = json.dumps(tr[k], ensure_ascii=False)[1:-1] if q == '"' else tr[k].replace('\\', '\\\\').replace(q, '\\' + q)
                        body = body.replace(q + esc + q, q + val + q)
                return m.group(1) + body + m.group(3)
            html = re.sub(r'(<script[^>]*>)(.*?)(</script>)', sub_scripts, html, flags=re.S)
            html = add_lang_ui(html, dst, lang, tr.get('Language', 'Language'))
            out = os.path.join(ROOT, lang, dst, 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(html)
        report[lang] = sorted(missing)
    # English originals get the switcher, hreflang links and the suggestion banner
    for src, dst in PAGES.items():
        p = os.path.join(ROOT, src); html = strip_lang_ui(open(p, encoding='utf-8').read())
        open(p, 'w', encoding='utf-8').write(add_lang_ui(html, dst, 'en', 'Language'))
    for lang, miss in report.items():
        print(f'{lang}: built {len(PAGES)} pages, {len(miss)} strings left in English')
        for k in miss[:15]:
            print('   ', k[:100])


if __name__ == '__main__':
    {'extract': extract, 'build': build}[sys.argv[1]]()
