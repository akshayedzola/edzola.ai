"""One-off accessibility fixes (WCAG 2.2 AA) across the public pages. Safe to re-run."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
files = [f for f in os.popen("find . -name '*.html' -not -path './.git/*' -not -path './team/*' -not -path './fundzola/*' -not -path './impactos-draft/*' -not -path './es/*' -not -path './pt/*'").read().split()]

SKIP_CSS = ('.gh-skip{position:absolute;left:16px;top:-60px;z-index:80;padding:10px 16px;border-radius:999px;'
            'background:#1A1A1A;color:#FDF8F4!important;font-weight:700;font-size:14px}.gh-skip:focus{top:12px}')
PAUSE_CSS = ('.motion-toggle{font:600 12px/1 "JetBrains Mono","IBM Plex Mono",ui-monospace,monospace;padding:8px 12px;'
             'border-radius:999px;border:1px solid #EADFD6;background:#fff;color:#1A1A1A;cursor:pointer}'
             '.motion-toggle:focus-visible{outline:3px solid #2C7771;outline-offset:2px}'
             '.is-paused .lane,.is-paused .org,.is-paused .reel-track{animation-play-state:paused!important}')
PAUSE_JS = ('<script id="motion-toggle">document.querySelectorAll(".motion-toggle").forEach(function(b){'
            'var host=document.querySelector(b.dataset.target);b.addEventListener("click",function(){'
            'var p=host.classList.toggle("is-paused");b.setAttribute("aria-pressed",p);b.textContent=p?b.dataset.play:b.dataset.pause;});});</script>')

for f in files:
    s = open(f, encoding='utf-8').read(); o = s
    # 1. contrast: deeper coral, red and mustard text colours (4.5:1 on every site background)
    s = re.sub(r'#(?:B4553A|B4533A)\b', '#9E452D', s, flags=re.I)
    s = re.sub(r'#C2412D\b', '#A8341F', s, flags=re.I)
    s = re.sub(r'#B7791F\b', '#8A5A12', s, flags=re.I)
    # 2. visible logo text is the accessible name
    s = s.replace(' aria-label="edzola.ai home"', '')
    # 3. skip link to the main content
    if 'class="gh-skip"' not in s and 'class="gh' in s:
        if re.search(r'<main\b', s):
            if not re.search(r'<main\b[^>]*\bid=', s):
                s = re.sub(r'<main\b', '<main id="main"', s, count=1)
            target = re.search(r'<main\b[^>]*\bid="([^"]+)"', s).group(1)
        else:
            m = re.search(r'<(article|section|div)\b(?![^>]*class="gh)[^>]*>', s[s.index('class="gh'):])
            target = 'main'
            s = re.sub(r'(<div class="gh[^"]*"[^>]*>.*?</details></div></div>)(\s*)<(article|section|div)\b', r'\1\2<\3 id="main"', s, count=1, flags=re.S)
        s = re.sub(r'(<div class="gh[^"]*"[^>]*>)', r'<a class="gh-skip" href="#%s">Skip to content</a>\1' % target, s, count=1)
        s = s.replace('<style id="gh-css">', '<style id="gh-css">\n' + SKIP_CSS, 1)
    # 4. how-nonprofits-operate already has its own banner (the reader bar)
    if 'how-nonprofits-operate' in f:
        s = s.replace('<div class="gh gh-static" role="banner">', '<div class="gh gh-static">')
    # 5. scrollable example lists in sector mock-ups are keyboard reachable
    s = re.sub(r'<div class="queue"(?![^>]*tabindex)', '<div class="queue" tabindex="0" role="region" aria-label="Example list (scrollable)"', s)
    # 6. sector tab panels: <article> may not take role=tabpanel; <section> may
    for m in reversed(list(re.finditer(r'<article(\b[^>]*role="tabpanel")', s))):
        start = m.start(); depth = 0
        for t in re.finditer(r'<(/?)article\b', s[start:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = start + t.start()
                s = s[:start] + '<section' + s[start+8:end] + '</section' + s[end+9:]
                break
    # 7. Patrons funding split is a list, not a table
    s = s.replace('class="stack-table" role="table"', 'class="stack-table" role="list"').replace('class="stack-row" role="row"', 'class="stack-row" role="listitem"')
    # 8. Sectors pager dots get a 24px target
    s = s.replace('.pager button{width:8px;height:8px;border-radius:50%;border:0;padding:0;',
                  '.pager button{width:24px;height:24px;border-radius:50%;border:0;padding:8px;background-clip:content-box!important;')
    s = s.replace('.pager button[aria-current="true"]{background:var(--coral);width:22px;border-radius:99px}',
                  '.pager button[aria-current="true"]{background:var(--coral);width:38px;border-radius:99px}')
    # 9. homepage footer headings follow the page outline
    if f == './index.html':
        s = s.replace('<h4>', '<h3>').replace('</h4>', '</h3>').replace('.footer h4{', '.footer h3{')
    # 10. pause controls for continuously moving strips (WCAG 2.2.2)
    if 'id="lane1"' in s and 'motion-toggle' not in s:
        s = s.replace('<span>A few of the teams we\'ve built and run systems with</span></div>',
                      '<span>A few of the teams we\'ve built and run systems with <button class="motion-toggle" data-target=".cloud" data-pause="Pause" data-play="Play" aria-pressed="false">Pause</button></span></div>', 1)
        s = s.replace('<div class="lane" id="lane1"></div>', '<div class="lane" id="lane1" tabindex="0" role="group" aria-label="Partner logos, row 1"></div>')
        s = s.replace('<div class="lane rev" id="lane2"></div>', '<div class="lane rev" id="lane2" tabindex="0" role="group" aria-label="Partner logos, row 2"></div>')
    if 'class="reel-window"' in s and 'motion-toggle' not in s:
        s = s.replace('<a href="https://www.youtube.com/@edzola/shorts" rel="noopener">All Shorts on YouTube →</a></div>',
                      '<span><button class="motion-toggle" data-target=".reels" data-pause="Pause" data-play="Play" aria-pressed="false">Pause</button> <a href="https://www.youtube.com/@edzola/shorts" rel="noopener">All Shorts on YouTube →</a></span></div>', 1)
    if 'motion-toggle' in s and 'id="motion-toggle"' not in s:
        s = s.replace('</head>', '<style>' + PAUSE_CSS + '</style>\n</head>', 1).replace('</body>', PAUSE_JS + '\n</body>', 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); print('fixed', f)
